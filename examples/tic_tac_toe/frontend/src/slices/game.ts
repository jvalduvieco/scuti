import {GameStage, GameState} from "../types";
import {createSlice} from "@reduxjs/toolkit";
import {acceptInvitation, boardUpdated, gameEnded, gameStarted, markPlaced, waitingForPlayerToPlay} from "../actions";
import {createGameCommandPending} from "../backend/apiSlice";

const initialState: GameState = {
  boardState: null,
  messages: [],
  stage: null,
  turn: null,
  winner: null,
  gameId: null
};

const gameSlice = createSlice({
  name: 'game',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
        .addCase(gameStarted, (state: GameState, action) => {
          if (state.gameId?.id === action.payload.gameId.id) {
            state.boardState = action.payload.board;
            state.stage = (action.payload.stage as GameStage);
            state.gameId = action.payload.gameId
            state.winner = null
          }
        })
        .addCase(markPlaced, (state, action) => {
          if (state.gameId?.id === action.payload.gameId.id) {
            state.messages.push(`Player ${action.payload.player.id} placed a mark on (${action.payload.x}, ${action.payload.y})`)
          }
        })
        .addCase(waitingForPlayerToPlay, (state: GameState, action) => {
          if (state.gameId?.id === action.payload.gameId.id) {
            state.turn = action.payload.playerId;
          }
        })
        .addCase(boardUpdated, (state: GameState, action) => {
          if (state.gameId?.id === action.payload.gameId.id) {
            state.boardState = action.payload.board
          }
        })
        .addCase(gameEnded, (state: GameState, action) => {
          if (state.gameId?.id === action.payload.gameId.id) {
            state.stage = action.payload.result;
            state.winner = action.payload.winner;
            state.messages = [];
            state.turn = null
          }
        })
        .addCase(acceptInvitation, (state: GameState, action) => {
          state.gameId = action.payload.game;})
        .addMatcher(createGameCommandPending, (state: GameState, action) => {
          state.gameId = action.meta.arg.originalArgs.gameId;
        })
  }
})

export const gameReducer = gameSlice.reducer
