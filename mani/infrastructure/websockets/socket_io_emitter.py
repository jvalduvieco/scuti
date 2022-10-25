import marshmallow_dataclass
import socketio
from injector import inject
from plum import dispatch

from mani.infrastructure.tools.string import camel_to_underscore
from applications.api.tools import to_javascript
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.effects import Event
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class EventToSocketIOBridge(EffectHandler):
    @inject
    def __init__(self, socketio_app: socketio.Server):
        self._socketio_app = socketio_app

    @dispatch
    def handle(self, event: Event) -> None:
        schema = marshmallow_dataclass.class_schema(event.__class__)()
        converted_event = {'type': camel_to_underscore(event.__class__.__name__).upper(),
                           'payload': to_javascript(schema.dump(event))}

        logger.debug("(Outer World) received event: %s", converted_event)
        self._socketio_app.emit('action', converted_event, broadcast=True)
