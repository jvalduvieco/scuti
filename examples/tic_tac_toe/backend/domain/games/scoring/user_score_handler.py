from dataclasses import replace

from domain.games.scoring.events import PlayerScoreChanged
from domain.games.scoring.user_score import UserScore
from domain.games.tic_tac_toe.events import GameEnded
from domain.users.events import UserCreated
from plum import dispatch

from scuti.domain.cqrs.bus.effect_handler import ManagedStateEffectHandler
from scuti.domain.cqrs.bus.state_management.condition import condition
from scuti.domain.cqrs.bus.state_management.effect_to_state_mapping import state_fetcher


class UserScoreHandler(ManagedStateEffectHandler):
    @dispatch
    def handle(self, effect: UserCreated):
        return UserScore(id=effect.user.id, score=0), []

    @dispatch
    @condition(lambda e: e.winner is not None)
    @state_fetcher(lambda e, r: r.by_id(e.winner))
    def handle(self, state: UserScore, effect: GameEnded):
        score = state.score + 100
        return replace(state, score=score), [PlayerScoreChanged(player_id=effect.winner, score=score)]
