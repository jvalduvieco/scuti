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
from mani.domain.cqrs.effects import Command, Event, Query, Effect
from mani.domain.model.modules import DomainModule
from mani.infrastructure.domain.cqrs.bus.effect_handlers.asynchronous_class import \
    build_asynchronous_class_effect_handler
from mani.infrastructure.domain.cqrs.bus.effect_handlers.synchronous_class import build_synchronous_class_effect_handler
from mani.infrastructure.domain.cqrs.cqrs_module import CQRSDomainModule
from mani.infrastructure.registering.inspection.plum_inspection import inspect
from mani.infrastructure.tools.list import unique
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
        [self.__register_handlers(build_asynchronous_class_effect_handler, self.command_bus, Command, handler)
         for handler in effect_handlers_to_inspect]
        [self.__register_handlers(build_asynchronous_class_effect_handler, self.event_bus, Event, handler)
         for handler in effect_handlers_to_inspect]
        [self.__register_handlers(build_synchronous_class_effect_handler, self.query_bus, Query, handler)
         for handler in effect_handlers_to_inspect]

    def __register_handlers(self, handler_builder: Callable, bus, base_effect: Type[Effect],
                            handler: Type[EffectHandler]):
        all_handler_parameters = inspect(handler.handle, should_ignore_self=True).values()
        effects = unique(flatten([handler_parameters[-1] for handler_parameters in all_handler_parameters]))
        [bus.subscribe(effect, handler_builder(handler, self.injector())) for effect in effects if
         base_effect in effect.__mro__]
