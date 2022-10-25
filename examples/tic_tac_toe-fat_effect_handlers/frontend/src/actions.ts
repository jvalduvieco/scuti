import {Action} from "redux";
import {BoardState, CellState, ConnectionStatus, GameStage, Id} from "./types";

export interface ConnectionStatusUpdated extends Action<"CONNECTION_STATUS_CHANGED"> {
  payload: {
    newStatus: ConnectionStatus
  }
}

export const connectionStatusUpdated = (newStatus: ConnectionStatus): ConnectionStatusUpdated => ({
  type: "CONNECTION_STATUS_CHANGED",
  payload: {
    newStatus
  }
});

export interface CreateNewGame extends Action<"CREATE_NEW_GAME"> {
  payload: {
    gameId: Id
    firstPlayer: Id
    secondPlayer: Id
    operationId: Id
  }
}

export const createNewGame = (gameId: Id, firstPlayer: Id, secondPlayer: Id, operationId: Id): CreateNewGame => ({
  type: "CREATE_NEW_GAME",
  payload: {
    gameId,
    firstPlayer,
    secondPlayer,
    operationId
  }
})


export interface PlaceMark extends Action<"PLACE_MARK"> {
  payload: {
    gameId: Id
    player: Id
    x: number
    y: number
    operationId: Id
  }
}

export const placeMark = (gameId: Id, player: Id, x: number, y: number, operationId: Id): PlaceMark => ({
  type: "PLACE_MARK",
  payload: {
    gameId,
    player,
    x,
    y,
    operationId
  }
})

export interface GameStarted extends Action<"GAME_STARTED"> {
  payload: {
    gameId: Id
    player1: Id
    player2: Id
    board: BoardState
    stage: GameStage
    parentOperationId: Id
  }
}

export interface BoardUpdated extends Action<"BOARD_UPDATED"> {
  payload: {
    gameId: Id
    board: CellState[][]
  }
}

export interface WaitingForPlayerPlay extends Action<"WAITING_FOR_PLAYER_PLAY"> {
  payload: {
    gameId: Id
    playerId: Id
  }
}

export interface GameEnded extends Action<"GAME_ENDED"> {
  payload: {
    gameId: Id
    winner: Id
    result: GameStage
  }
}
