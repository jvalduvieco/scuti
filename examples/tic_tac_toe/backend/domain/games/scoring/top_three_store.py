from abc import ABC

from domain.games.scoring.top_three_list import TopThreeList
from mani.domain.model.store.store import Store


class TopThreeStore(Store[TopThreeList], ABC):
    pass
