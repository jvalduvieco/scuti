from enum import Enum


class GameErrorReasons(Enum):
    POSITION_OFF_LIMITS = "POSITION_OFF_LIMITS"
    PLAYER_CAN_NOT_PLAY = "PLAYER_CAN_NOT_PLAY"
    POSITION_ALREADY_FILLED = "POSITION_ALREADY_FILLED"

class GameStage(Enum):
    PLAYER_WON = "PLAYER_WON"
    DRAW = "DRAW"
    IN_PROGRESS = "IN_PROGRESS"
