import logging
import signal
import sys
from threading import Thread
from typing import List, Type

import flask_injector
import socketio
from applications.api.controllers import command_controller, event_controller, query_controller
from applications.api.tools import from_javascript
from applications.api.websockets.create_socket_io_app import create_socketio_app
from applications.api.websockets.sessions.session_repository import SessionRepository
from applications.api.websockets.socket_io_emitter import EventToSocketIOBridge
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.events import BusHandlerFailed
from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.effects import Command, Event, Query
from mani.domain.model.application.domain_application import DomainApplication
from mani.domain.model.application.net_config import NetConfig
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.asynchronous_class import \
    build_asynchronous_class_effect_handler
from mani.infrastructure.logging.get_logger import get_logger
from mani.infrastructure.serialization.from_untyped_dict import from_untyped_dict
from mani.infrastructure.tools.string import snake_to_upper_camel

logger = get_logger(__name__)


class CQRSAPIApp:
    def __init__(self, domain_app: DomainApplication, config: NetConfig, accepted_commands: List[Type[Command]] = None,
                 events_to_publish: List[Type[Event]] = None, accepted_events: List[Type[Event]] = None,
                 accepted_queries: List[Type[Query]] = None,
                 bus_error_effect_handler: Type[EffectHandler] = None):
        self._available_commands = {command_type.__name__: command_type for command_type in accepted_commands or []}
        self._available_events = {event_type.__name__: event_type for event_type in accepted_events or []}
        self._available_queries = {query_type.__name__: query_type for query_type in accepted_queries or []}
        self._events_to_publish = events_to_publish or []
        self._thread_instances: List[Thread] = []
        self._domain_app = domain_app
        self._config = config

        def signal_handler(sig, frame):
            logger.info("Stop requested")
            self._domain_app.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        injector = domain_app.injector()
        get_logger("engineio").setLevel(logging.ERROR)
        get_logger("werkzeug").setLevel(logging.ERROR)
        self._api_app = Flask(__name__)
        self._api_app.config["SECRET_KEY"] = "secret!"
        CORS(self._api_app, resources={r"/*": {"origins": "*"}})
        Compress(self._api_app)
        flask_injector.FlaskInjector(app=self._api_app, injector=injector)
        domain_app.event_bus.subscribe(BusHandlerFailed,
                                       build_asynchronous_class_effect_handler(bus_error_effect_handler, None,
                                                                               injector))
        [domain_app.event_bus.subscribe(event,
                                        build_asynchronous_class_effect_handler(EventToSocketIOBridge, None, injector))
         for event in events_to_publish]

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
        self._socketio_app = create_socketio_app(self._api_app)
        session_repository = self._domain_app.injector().get(SessionRepository)
        self._socketio_app.on("action",
                              lambda s, m: self.__handle_websocket_actions(s, m))
        self._socketio_app.on("disconnect",
                              lambda s: self.__handle_websocket_actions(s, self._create_disconnect_action(s)))

        injector.binder.bind(socketio.Server, self._socketio_app)

    def _create_disconnect_action(self, s: str):
        return {
            "type": "server/SESSION_DISCONNECTED",
            "data": {
                "sessionId": s
            }}

    def __user_disconnected(self, repository: SessionRepository, sid: str):
        logger.debug(f"Removing session {sid}")
        repository.remove(sid)

    def __handle_websocket_actions(self, sid: str, message: dict):
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
        self._domain_app.start()
        self._api_app.run(threaded=True, host=self._config.host, port=self._config.port, debug=False)

    def stop(self):
        self._domain_app.stop()
