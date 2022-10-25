
from mani.domain.cqrs.bus.bus_handler_failed import BusHandlerFailed
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class BusErrorHandler(EffectHandler):
    def handle(self, effect: BusHandlerFailed):
        logger.error(f"{effect.error} on: {effect.stack_trace} while handling {effect.effect}")
