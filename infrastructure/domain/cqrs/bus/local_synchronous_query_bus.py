from domain.cqrs.effects import Query
from domain.cqrs.bus.query_bus import QueryBus
from domain.cqrs.bus.query_handler import QueryHandler
from infrastructure.domain.cqrs.bus.local_synchronous_bus import LocalSynchronousBus


class LocalSynchronousQueryBus(LocalSynchronousBus[Query, QueryHandler], QueryBus):
    pass
