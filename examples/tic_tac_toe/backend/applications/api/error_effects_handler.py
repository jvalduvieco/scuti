from scuti.domain.cqrs.bus.effect_handler import EffectHandler
from scuti.domain.cqrs.bus.events import BusHandlerFailed, InfrastructureError
from scuti.domain.model.application.application_error import ApplicationError
from scuti.infrastructure.logging.errors import print_traceback
from scuti.infrastructure.logging.get_logger import get_logger
from plum import dispatch

logger = get_logger(__name__)


class ErrorEffectsHandler(EffectHandler):
    """
    This effect handler is called when an error of the given types is handled by the bus
    """
    @dispatch
    def handle(self, effect: BusHandlerFailed | InfrastructureError | ApplicationError):
        logger.error(f"{effect.error}{f'while processing {effect.effect}' if hasattr(effect, 'effect') else ''} in {effect.stack_trace}")
        print_traceback(logger, effect.stack_trace)
