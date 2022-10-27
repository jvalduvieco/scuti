import logging
from threading import Thread
from typing import List, Type

import flask_injector
import socketio
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from applications.api.controllers import command_controller, query_controller, event_controller
from mani.domain.cqrs.bus.bus_handler_failed import BusHandlerFailed
from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.effects import Command, Event, Query
from mani.domain.model.application.domain_application import DomainApplication
from mani.domain.model.application.net_config import NetConfig
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.asynchronous_class import \
    build_asynchronous_class_effect_handler
from mani.infrastructure.logging.get_logger import get_logger
from mani.infrastructure.tools.thread import spawn
from applications.api.websockets.create_socket_io_app import create_socketio_app
from applications.api.websockets.socket_io_emitter import EventToSocketIOBridge

logger = get_logger(__name__)


class CQRSAPIApp:
    def __init__(self, domain_app: DomainApplication, config: NetConfig, accepted_commands: List[Type[Command]] = None,
                 events_to_publish: List[Type[Event]] = None, accepted_events: List[Type[Event]] = None,
                 accepted_queries: List[Type[Query]] = None,
                 bus_error_effect_handler: Type[EffectHandler] = None):
        self._accepted_commands = accepted_commands or []
        self._events_to_publish = events_to_publish or []
        self._accepted_events = accepted_events or []
        self._accepted_queries = accepted_queries or []
        self._thread_instances: List[Thread] = []
        self._domain_app = domain_app
        self._config = config

        injector = domain_app.injector()
        get_logger("engineio").setLevel(logging.ERROR)
        get_logger("werkzeug").setLevel(logging.ERROR)
        self._api_app = Flask(__name__)
        self._api_app.config["SECRET_KEY"] = "secret!"
        CORS(self._api_app, resources={r"/*": {"origins": "*"}})
        Compress(self._api_app)
        flask_injector.FlaskInjector(app=self._api_app, injector=injector)
        domain_app.event_bus.subscribe(BusHandlerFailed,
                                       build_asynchronous_class_effect_handler(bus_error_effect_handler, injector))
        [domain_app.event_bus.subscribe(event, build_asynchronous_class_effect_handler(EventToSocketIOBridge, injector))
         for event in events_to_publish]

        self._api_app.add_url_rule("/commands",
                                   view_func=command_controller(injector.get(CommandBus), self._accepted_commands),
                                   provide_automatic_options=None,
                                   methods=["POST"])
        self._api_app.add_url_rule("/queries",
                                   view_func=query_controller(injector.get(QueryBus), self._accepted_queries),
                                   provide_automatic_options=None,
                                   methods=["POST"])
        self._api_app.add_url_rule("/events",
                                   view_func=event_controller(injector.get(EventBus), self._accepted_events),
                                   provide_automatic_options=None,
                                   methods=["POST"])
        self._socketio_app = create_socketio_app(self._api_app)
        injector.binder.bind(socketio.Server, self._socketio_app)

    def start(self):
        self._thread_instances += [spawn(CQRSAPIApp._bus_runner, self._domain_app.injector().get(AsynchronousBus))]
        self._api_app.run(threaded=True, host=self._config.host, port=self._config.port, debug=False)

    def stop(self):
        [thread.join() for thread in self._thread_instances]

    @staticmethod
    def _bus_runner(bus: AsynchronousBus):
        logger.info("Sequential bus runner starting...")
        while True:
            bus.drain(should_block=True)
