from mani.domain.cqrs.bus.hooks.bus_hook import BusHook
from mani.domain.cqrs.effects import Effect
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class LoggingEffectsBusHook(BusHook):

    def on_handle(self, effect: Effect):
        logger.info(f"handling: {effect}")
