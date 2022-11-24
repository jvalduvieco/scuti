from scuti.domain.cqrs.bus.hooks.bus_hook import BusHook
from scuti.domain.cqrs.effects import Effect
from scuti.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class LoggingEffectsBusHook(BusHook):

    def on_handle(self, effect: Effect):
        logger.info(f"handling: {effect}")
