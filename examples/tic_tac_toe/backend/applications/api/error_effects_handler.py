from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.events import BusHandlerFailed, InfrastructureError
from mani.domain.model.application.application_error import ApplicationError
from mani.infrastructure.logging.errors import print_traceback
from mani.infrastructure.logging.get_logger import get_logger
from plum import dispatch

logger = get_logger(__name__)


class ErrorEffectsHandler(EffectHandler):
    @dispatch
    def handle(self, effect: BusHandlerFailed | InfrastructureError | ApplicationError):
        logger.error(f"{effect.error} while handling {effect.effect}")
        print_traceback(logger, effect.stack_trace)
