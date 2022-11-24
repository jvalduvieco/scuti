from typing import List, Type, Tuple

from domain.games.scoring.top_three_list_handler import TopThreeHandler
from domain.games.scoring.top_three_store import TopThreeStore
from domain.games.scoring.user_score_handler import UserScoreHandler
from domain.games.scoring.user_score_repository import UserScoreRepository
from infrastructure.domain.games.scoring.top_three_store_in_memory import TopThreeStoreInMemory
from infrastructure.domain.games.scoring.user_score_repository_in_memory import UserScoreRepositoryInMemory
from injector import Module, Scope, SingletonScope

from scuti.domain.model.modules import DomainModule


class ScoringDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [
            (UserScoreRepository, UserScoreRepositoryInMemory, SingletonScope),
            (TopThreeStore, TopThreeStoreInMemory, SingletonScope)
        ]

    def effect_handlers(self):
        return [
            (UserScoreHandler, UserScoreRepository),
            (TopThreeHandler, TopThreeStore)
        ]
