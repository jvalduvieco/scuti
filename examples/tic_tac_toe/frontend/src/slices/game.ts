import {GameStage, GameState} from "../types";
import {createSlice} from "@reduxjs/toolkit";
import {
  acceptInvitation,
  boardUpdated,
  createGame,
  gameCreated,
  gameEnded,
  gameStarted,
  placeMark,
  waitingForPlayerToPlay
} from "../actions";
import {apiSlice, userJoined} from "../backend/apiSlice";

const initialState: GameState = {
  boardState: null,
  messages: [],
  stage: null,
  turn: null,
  winner: null,
  gameId: null,
  firstPlayer: null,
  secondPlayer: null
};

const gameSlice = createSlice({
  name: 'game',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
        .addCase(createGame.pending, (state: GameState, action) => {
          state.gameId = action.meta.arg.gameId;
          state.firstPlayer = action.meta.arg.creator;
        })
        .addCase(gameStarted, (state: GameState, action) => {
          if (state.gameId?.id === action.payload.gameId.id) {
            state.boardState = action.payload.board;
            state.stage = (action.payload.stage as GameStage);
            state.gameId = action.payload.gameId
          }
        })
        .addCase(placeMark.fulfilled, (state, action) => {
          if (state.gameId?.id === action.meta.arg.gameId.id) {
            state.messages.push(`Player ${action.meta.arg.player.id} placed a mark on (${action.meta.arg.x}, ${action.payload.y})`)
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
          state.gameId = action.payload.game;
          state.firstPlayer = action.payload.host;
          state.secondPlayer = action.payload.invited;
        })
  }
})

export const gameReducer = gameSlice.reducer
