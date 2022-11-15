from dataclasses import replace

from domain.games.tic_tac_toe.events import GameEnded
from domain.users.events import UserCreated
from mani.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from mani.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher
from mani.infrastructure.domain.cqrs.bus.build_effect_handlers.state_managing_effect_handler import NotInterested
from plum import dispatch
from domain.games.scoring.user_score import UserScore
from domain.games.scoring.events import PlayerScoreChanged


class UserScoreHandler(ManagedStateEffectHandler):
    @dispatch
    def handle(self, effect: UserCreated):
        return UserScore(id=effect.user.id, score=0), []

    @dispatch
    @state_fetcher(lambda e, r: r.by_id(e.winner) if e.winner is not None else NotInterested())
    def handle(self, state: UserScore, effect: GameEnded):
        score = state.score + 100
        return replace(state, score=score), [PlayerScoreChanged(player_id=effect.winner, score=score)]
