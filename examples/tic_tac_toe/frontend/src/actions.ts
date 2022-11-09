import {BoardState, CellState, ConnectionStatus, GameStage, Id, withPayloadType} from "./types";
import TicTacToeBackendClient from "./backend/TicTacToeBackendClient";
import {createOperationId} from "./tools/id";
import {createAction, createAsyncThunk} from "@reduxjs/toolkit";

export const connectionStatusUpdated = createAction('CONNECTION_STATUS_CHANGED',
    withPayloadType<{
      newStatus: ConnectionStatus
    }>())

export const placeMark = createAsyncThunk('game/placeMark', async (payload: { gameId: Id, player: Id, x: number, y: number }) => {
  await TicTacToeBackendClient.placeMark(
      payload.gameId,
      payload.player,
      payload.x,
      payload.y,
      createOperationId())
  return payload;
})

export const createNewGame = createAsyncThunk('game/createNewGame', async (payload: { gameId: Id, firstPlayer: Id, secondPlayer: Id }) => {
  await TicTacToeBackendClient.createNewGame(
      payload.gameId,
      payload.firstPlayer,
      payload.secondPlayer,
      createOperationId())
  return payload;
})


export const gameStarted = createAction('GAME_STARTED',
    withPayloadType<{
      gameId: Id
      player1: Id
      player2: Id
      board: BoardState
      stage: GameStage
      parentOperationId: Id
    }>())

export const newGameCreated = createAction('NEW_GAME_CREATED',
    withPayloadType<{
      gameId: Id
      firstPlayer: Id
      secondPlayer: Id
    }>())

export const waitingForPlayerToPlay = createAction('WAITING_FOR_PLAYER_PLAY',
    withPayloadType<{
      gameId: Id
      playerId: Id
    }>())

export const boardUpdated = createAction('BOARD_UPDATED',
    withPayloadType<{
      gameId: Id
      board: CellState[][]
    }>())

export const gameEnded = createAction('GAME_ENDED',
    withPayloadType<{
      gameId: Id
      winner: Id
      result: GameStage
    }>())

export const topThreeListUpdated= createAction('TOP_THREE_LIST_UPDATED')
