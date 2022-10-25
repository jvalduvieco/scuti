from typing import Type, List

from flask import request

from applications.api.tools import from_javascript, to_message_response, to_javascript
from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.effects import Command, Query, Event
from mani.infrastructure.logging.get_logger import get_logger
from mani.infrastructure.serialization.from_untyped_dict import from_untyped_dict

logger = get_logger(__name__)


def command_controller(command_bus: CommandBus, accepted_commands: List[Type[Command]]):
    available_commands = {command_type.__name__: command_type for command_type in accepted_commands}

    def dispatch_command_request():
        client_request = request.get_json()
        logger.debug("Command received: %s", client_request["command"])
        try:
            command = from_untyped_dict(available_commands[client_request['command']["type"]],
                                        from_javascript(client_request['command']["payload"]))
        except KeyError:
            logger.warning(f"(Domain) Received unknown command: {client_request['command']}")
            return f"Unknown command: {client_request['command']}", 400
        except Exception as err:
            logger.error(f"Invalid command payload: {client_request['command']}")
            raise err
        command_bus.handle(command)
        return to_message_response("OK"), 200

    return dispatch_command_request


def query_controller(query_bus: QueryBus, accepted_queries: List[Type[Query]]):
    available_queries = {query_type.__name__: query_type for query_type in accepted_queries}

    def dispatch_query_request():
        client_request = request.get_json()
        logger.debug("Query received: %s", client_request["query"])

        try:
            query = from_untyped_dict(available_queries[client_request['query']["type"]],
                                      from_javascript(client_request['query'].get("payload", {})))
        except KeyError:
            logger.warning(f"Received unknown query: {client_request['query']}")
            return f"Unknown query: {client_request['query']}", 400
        except Exception as err:
            logger.error(f"Invalid query payload: {client_request['query']}")
            raise err

        result = query_bus.handle(query)
        return to_javascript(result), 200

    return dispatch_query_request


def event_controller(event_bus: EventBus, accepted_events: List[Type[Event]]):
    available_events = {event_type.__name__: event_type for event_type in accepted_events}

    def dispatch_event_request():
        client_request = request.get_json()
        logger.debug("Event received: %s", client_request["event"])
        try:
            event = from_untyped_dict(available_events[client_request['event']["type"]],
                                      from_javascript(client_request['event'].get("payload", {})))
        except KeyError:
            logger.warning(f"(Domain) Received unknown event: {client_request['event']}")
            return f"Unknown event: {client_request['event']}", 400
        except Exception as err:
            logger.error(f"Invalid event payload: {client_request['event']}")
            raise err

        event_bus.handle([event])
        return to_message_response("OK"), 200

    return dispatch_event_request
