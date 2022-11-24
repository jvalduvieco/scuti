from domain.games.scoring.events import PlayerScoreChanged, TopThreeListUpdated
from domain.games.scoring.queries import GetTopThreePlayers
from domain.games.scoring.top_three_list import TopThreeList
from plum import dispatch

from scuti.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher, Singleton


class TopThreeHandler(ManagedStateEffectHandler):
    @dispatch
    @state_fetcher(Singleton)
    def handle(self, top_three_list: TopThreeList | None, effect: PlayerScoreChanged):
        if not top_three_list:
            top_three_list = TopThreeList()
        if top_three_list.should_be_on_the_list(effect.score):
            current_top_three = top_three_list.include(effect.player_id, effect.score)
            return current_top_three, [TopThreeListUpdated(previous=top_three_list, current=current_top_three)]
        else:
            return top_three_list, []

    @dispatch
    @state_fetcher(Singleton)
    def handle(self, top_three_list: TopThreeList | None, query: GetTopThreePlayers):
        result = top_three_list.top_three if top_three_list is not None else []
        return {"list": result, "parent_operation_id": query.operation_id}
