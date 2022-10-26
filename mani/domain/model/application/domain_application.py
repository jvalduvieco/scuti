from collections.abc import Mapping
from functools import cached_property
from threading import Thread
from typing import List, Type, Optional, Dict, Callable

from injector import Injector, Scope
from setuptools.namespaces import flatten

from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import effect_to_state_mapper_property
from mani.domain.cqrs.effects import Command, Event, Query, Effect
from mani.domain.model.modules import DomainModule
from mani.domain.model.repository.repository import Repository
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.asynchronous_class import \
    build_asynchronous_class_effect_handler
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.state_managing_effect_handler import \
    build_asynchronous_state_managing_class_effect_handler
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.synchronous_class import \
    build_synchronous_class_effect_handler
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.synchronous_state_managing_effect_handler import \
    build_synchronous_state_managing_class_effect_handler
from mani.infrastructure.domain.cqrs.cqrs_module import CQRSDomainModule
from mani.infrastructure.registering.inspection.plum_inspection import inspect, InspectionResult
from mani.infrastructure.tools.thread import spawn


class DomainApplication:
    def __init__(self,
                 config: Mapping,
                 domains: List[Type[DomainModule]] = None,
                 injector: Optional[Injector] = None):
        domains = domains if domains is not None else []
        self.__application_config = config
        self.__domains: List[Type[DomainModule]] = [CQRSDomainModule] + domains
        self.__domain_instances: Dict[Type[DomainModule], DomainModule] = self.__instantiate_domain_modules()
        self.__injector: Injector = injector if injector is not None else self.__build_injector()
        self.__threads_instances: List[Thread] = []
        self.__register_effect_handlers()

    def start(self):
        self.__threads_instances = self.__start_modules_threads()
        self.__run_module_init_commands()

    def injector(self) -> Injector:
        return self.__injector

    def config(self) -> Mapping:
        return self.__application_config

    def stop(self):
        for thread in self.__threads_instances:
            thread.join()

    @cached_property
    def command_bus(self) -> CommandBus:
        return self.__injector.get(CommandBus)

    @cached_property
    def event_bus(self) -> EventBus:
        return self.__injector.get(EventBus)

    @cached_property
    def query_bus(self) -> QueryBus:
        return self.__injector.get(QueryBus)

    def __str__(self):
        return f"This is an app running these domains: {', '.join([domain.__name__ for domain in self.__domain_instances.keys()])}"

    def __build_injector(self):
        def build_custom_binder(interface_type: Type, concrete_type: Type, scope: Scope):
            def bind(binder):
                binder.bind(interface_type, concrete_type, scope)

            return bind

        binding_definitions = list(flatten([instance.bindings() for instance in self.__domain_instances.values()]))
        adapted_bindings = [build_custom_binder(*binding) if isinstance(binding, tuple) else binding
                            for binding in binding_definitions]
        injector = Injector(adapted_bindings)
        return injector

    def __instantiate_domain_modules(self) -> Dict[Type[DomainModule], DomainModule]:
        return {module: module(self.__application_config) for module in self.__domains if
                issubclass(module, DomainModule)}

    def __start_modules_threads(self) -> List[Thread]:
        result = []
        for thread in flatten([module.processes() for module in self.__domain_instances.values()]):
            result += [spawn(thread)]
        return result

    def __run_module_init_commands(self):
        all_initial_commands = list(flatten([module.init_commands() for module in self.__domain_instances.values()]))
        [self.command_bus.handle(command) for command in all_initial_commands]

    def __register_effect_handlers(self):
        effect_handlers_to_inspect = list(
            flatten([module.effect_handlers() for module in self.__domain_instances.values()]))
        if not effect_handlers_to_inspect:
            return
        # TODO externalize builder selection to a config?
        for handler_type in effect_handlers_to_inspect:
            if type(handler_type) is tuple:
                handler_type, repository = handler_type
                async_builder = build_asynchronous_state_managing_class_effect_handler
                sync_builder = build_synchronous_state_managing_class_effect_handler
            else:
                repository = None
                async_builder = build_asynchronous_class_effect_handler
                sync_builder = build_synchronous_class_effect_handler
            self.__register_handlers(async_builder, self.command_bus, Command, handler_type, repository)
            self.__register_handlers(async_builder, self.event_bus, Event, handler_type, repository)
            self.__register_handlers(sync_builder, self.query_bus, Query, handler_type, repository)

    def __register_handlers(self, handler_builder: Callable,
                            bus,
                            base_effect: Type[Effect],
                            handler: Type[EffectHandler],
                            repository: Optional[Type[Repository]]):
        all_handler_parameters = inspect(handler.handle, should_ignore_self=True,
                                         annotations_to_retrieve=[effect_to_state_mapper_property]).values()
        for method in all_handler_parameters:
            if repository is None:
                self.__register_effect_handler_without_repository(base_effect, bus, method, handler, handler_builder)
            else:
                self.__register_effect_handler_with_repository(base_effect, bus, method, handler, handler_builder,
                                                               repository)

    def __register_effect_handler_without_repository(self, base_effect: Type[Effect],
                                                     bus,
                                                     method: InspectionResult,
                                                     handler: Type[EffectHandler],
                                                     handler_builder: Callable):
        for effect in method.parameter_types[-1]:
            if base_effect in effect.__mro__:
                bus.subscribe(effect, handler_builder(handler, self.injector()))

    def __register_effect_handler_with_repository(self, base_effect: Type[Effect],
                                                  bus,
                                                  method: InspectionResult,
                                                  handler: Type[EffectHandler],
                                                  handler_builder: Callable,
                                                  repository: Type[Repository]):
        state_mapper = method.annotations.get(effect_to_state_mapper_property, None)
        for effect in method.parameter_types[-1]:
            if base_effect in effect.__mro__:
                bus.subscribe(effect, handler_builder(handler, repository, state_mapper, self.injector()))
