import {BoardState, CellState, ConnectionStatus, GameStage, Id, User, withPayloadType} from "./types";
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

export const createGame = createAsyncThunk('game/CreateGame', async (payload: { gameId: Id, creator: Id }) => {
  await TicTacToeBackendClient.createGame(
      payload.gameId,
      payload.creator,
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

export const gameCreated = createAction('GAME_CREATED',
    withPayloadType<{
      gameId: Id
      creator: Id
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

export const userConnected = createAction<User>('USER_CONNECTED')
export const userInvited = createAction<{host: Id, invited: Id, game: Id}>('USER_INVITED')
export const acceptInvitation = createAction<{host: Id, invited: Id, game: Id}>('ACCEPT_INVITATION')
export const choseOpponent = createAction<User>('CHOSE_OPPONENT')
export const UsersOnlineUpdated = createAction('USERS_ONLINE_UPDATED')
export const topThreeListUpdated = createAction('TOP_THREE_LIST_UPDATED')
