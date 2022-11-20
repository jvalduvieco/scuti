from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.events import BusHandlerFailed
from mani.infrastructure.logging.errors import print_traceback
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class BusErrorHandler(EffectHandler):
    def handle(self, effect: BusHandlerFailed):
        logger.error(f"{effect.error} while handling {effect.effect}")
        print_traceback(logger, effect.stack_trace)
