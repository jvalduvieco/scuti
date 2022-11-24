from dataclasses import dataclass

from scuti.domain.model.application.net_config import NetConfig


@dataclass(frozen=True)
class TicTacToeConfig(NetConfig):
    pass
