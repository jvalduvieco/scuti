from domain.games.scoring.top_three_list import TopThreeList
from domain.games.scoring.top_three_store import TopThreeStore

from scuti.infrastructure.domain.model.store.in_memory_store import InMemoryStore


class TopThreeStoreInMemory(InMemoryStore[TopThreeList], TopThreeStore):
    pass
