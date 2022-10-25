from mani.domain.cqrs.bus.query_bus import QueryBus
from mani.domain.cqrs.effects import Query
from mani.infrastructure.domain.cqrs.bus.local_synchronous_bus import LocalSynchronousBus


class LocalSynchronousQueryBus(LocalSynchronousBus, QueryBus):
    pass
