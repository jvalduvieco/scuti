import logging
import signal
import sys
from threading import Thread
from typing import List, Type

import flask_injector
import socketio
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from applications.api.controllers import command_controller, event_controller, query_controller
from applications.api.tools import from_javascript
from applications.api.websockets.create_socket_io_app import create_socketio_app
from applications.api.websockets.socket_io_emitter import EventToSocketIOBridge
from scuti.domain.cqrs.bus.command_bus import CommandBus
from scuti.domain.cqrs.bus.event_bus import EventBus
from scuti.domain.cqrs.bus.query_bus import QueryBus
from scuti.domain.cqrs.effects import Command, Event, Query
from scuti.domain.model.application.application_error import ApplicationError
from scuti.domain.model.application.domain_application import DomainApplication
from scuti.domain.model.application.net_config import NetConfig
from scuti.domain.model.modules import DomainModule
from scuti.infrastructure.domain.cqrs.bus.build_effect_handlers.asynchronous_class import \
    build_asynchronous_class_effect_handler
from scuti.infrastructure.logging.get_logger import get_logger
from scuti.infrastructure.serialization.from_untyped_dict import from_untyped_dict
from scuti.infrastructure.tools.string import snake_to_upper_camel

logger = get_logger(__name__)


class CQRSAPIApp:
    """
    This class allows the user to fully customize how the domain model is wired to user infrastructure. It's
    responsibility to Scuti are:
     - Creating the `DomainApplication`
     - provide required configuration
     - Notify start or stop events
     - Feed effects
     - Emit effects
    """
    def __init__(self, domains: List[Type[DomainModule]], config: NetConfig,
                 accepted_commands: List[Type[Command]] = None,
                 events_to_publish: List[Type[Event]] = None,
                 accepted_events: List[Type[Event]] = None,
                 accepted_queries: List[Type[Query]] = None):
        self._available_commands = {command_type.__name__: command_type for command_type in accepted_commands or []}
        self._available_events = {event_type.__name__: event_type for event_type in accepted_events or []}
        self._available_queries = {query_type.__name__: query_type for query_type in accepted_queries or []}
        self._events_to_publish = events_to_publish or []
        self._thread_instances: List[Thread] = []
        self._config = config
        """
        This is de domain application. Offers a minimal api consumed by your application that enables accepting 
        effects and emitting events to the outside.
        """
        self._domain_app = DomainApplication(domains=domains, config=config.__dict__)

        # Let's die with some dignity
        def signal_handler(sig, frame):
            logger.info("Stop requested")
            self._domain_app.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)

        # Boring Flask stuff
        get_logger("engineio").setLevel(logging.ERROR)
        get_logger("werkzeug").setLevel(logging.ERROR)
        self._api_app = Flask(__name__)
        self._api_app.config["SECRET_KEY"] = "VeryS3cret1275"
        CORS(self._api_app, resources={r"/*": {"origins": "*"}})
        Compress(self._api_app)
        # The injector is the core of our domain model. Holds all dependencies and enables building all required objects
        injector = self._domain_app.injector()
        flask_injector.FlaskInjector(app=self._api_app, injector=injector)
        # There are standard Flask controllers used to receive effects from other systems. See [[controllers.py]]
        self._api_app.add_url_rule("/commands",
                                   view_func=command_controller(injector.get(CommandBus), self._available_commands),
                                   provide_automatic_options=None,
                                   methods=["POST"])
        self._api_app.add_url_rule("/queries",
                                   view_func=query_controller(injector.get(QueryBus), self._available_queries),
                                   provide_automatic_options=None,
                                   methods=["POST"])
        self._api_app.add_url_rule("/events",
                                   view_func=event_controller(injector.get(EventBus), self._available_events),
                                   provide_automatic_options=None,
                                   methods=["POST"])

        # Have a fallback error manager, this should never be called as Scuti captures all exceptions
        self._api_app.register_error_handler(Exception, self.__handle_internal_error)

        # Configure socket.io server
        self._socketio_app = create_socketio_app(self._api_app)

        # Allow commands to come via websockets, this is explained below
        self._socketio_app.on("action", lambda s, m: self.__handle_websocket_actions(s, m))

        # Manage socket.io disconnections so we can handle a domain event that sets the user as offline
        self._socketio_app.on("disconnect",
                              lambda s: self.__handle_websocket_actions(s, self.__create_disconnect_action(s)))

        injector.binder.bind(socketio.Server, self._socketio_app)

        # Make sure that all events that are sent to other domains are published using our system of choice
        [self._domain_app.event_bus.subscribe(event,
                                              build_asynchronous_class_effect_handler(EventToSocketIOBridge,
                                                                                      None,
                                                                                      injector))
         for event in events_to_publish]

    def __handle_internal_error(self, error: Exception, http_status_code: int = 500):
        """
        Errors are sent to the event bus to an effect handler can act on an error
        """
        response_body = """{"application_error": {"status_code": %d ,"message": "%s"}}""" % (
            http_status_code, error.__str__())
        self._domain_app.event_bus.handle(ApplicationError(error=str(error), stack_trace=error.__traceback__))
        return response_body, http_status_code

    def __create_disconnect_action(self, s: str):
        """
        Simulate a session disconnected action coming from the frontend in case of a websocket disconnection
        """
        return {
            "type": "server/SESSION_DISCONNECTED",
            "data": {
                "sessionId": s
            }}

    def __handle_websocket_actions(self, sid: str, message: dict):
        """
        In this case we are receiving `AssociateUserToSession` command using socket.io websocket so we can obtain
        session id and register that session Id with a user. Commands / events could also come using websockets so
        here `Commands` or `Events` are created and handled by the corresponding bus. Made as an example.
        """
        logger.debug(f"action received: {sid} {message}")
        message["type"] = snake_to_upper_camel(message["type"].split("/")[1])
        if message["type"] == "AssociateUserToSession":
            message = self.__add_session_id(message, sid)
        bus = None
        effect_type = None
        if message["type"] in self._available_commands:
            bus = self._domain_app.command_bus
            effect_type = self._available_commands[message["type"]]
        elif message["type"] in self._available_events:
            bus = self._domain_app.event_bus
            effect_type = self._available_events[message["type"]]
        effect = from_untyped_dict(effect_type, from_javascript(message["data"]))
        bus.handle(effect)

    def __add_session_id(self, message: dict, session_id: str):
        return {**message, "data": {**message["data"], "sessionId": session_id}}

    def start(self):
        """
        Start the app. Notify all interested parties
        """
        self._domain_app.start()
        self._api_app.run(threaded=True, host=self._config.host, port=self._config.port, debug=False)

    def stop(self):
        """
        Stop the app. Notify all interested parties
        """
        self._domain_app.stop()
