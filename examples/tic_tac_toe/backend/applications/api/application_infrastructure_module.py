from typing import Any, List, Tuple, Type

from applications.api.error_effects_handler import ErrorEffectsHandler
from applications.api.websockets.sessions.session_repository import SessionRepository
from applications.api.websockets.sessions.session_repository_in_memory import SessionRepositoryInMemory
from applications.api.websockets.socket_io_manager import SocketIOManager
from injector import Binder, Module, Scope, SingletonScope
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.model.modules import DomainModule


class ApplicationModule(Module):
    def configure(self, binder: Binder):
        binder.bind(SessionRepository, SessionRepositoryInMemory, scope=SingletonScope)


class ApplicationInfrastructureModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type[Any], Type[Any], Type[Scope]]]:
        return [ApplicationModule]

    def effect_handlers(self) -> List[Type[EffectHandler]]:
        return [SocketIOManager,
                ErrorEffectsHandler]
