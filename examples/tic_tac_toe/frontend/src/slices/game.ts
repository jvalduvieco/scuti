import {GameStage, GameState} from "../types";
import {createSlice} from "@reduxjs/toolkit";
import {acceptInvitation, boardUpdated, gameEnded, gameStarted, markPlaced, waitingForPlayerToPlay} from "../actions";
import {createGameCommandPending} from "../backend/apiSlice";
import isEqual from "lodash.isequal";

const initialState: GameState = {
    boardState: null,
    messages: [],
    stage: null,
    turn: null,
    winner: null,
    gameId: null,
    timeout: null
};

const gameSlice = createSlice({
    name: 'game',
    initialState,
    reducers: {},
    extraReducers(builder) {
        builder
            .addCase(gameStarted, (state: GameState, action) => {
                if (isEqual(state.gameId, action.payload.gameId)) {
                    state.boardState = action.payload.board;
                    state.stage = (action.payload.stage as GameStage);
                    state.gameId = action.payload.gameId
                    state.winner = null
                }
            })
            .addCase(markPlaced, (state, action) => {
                if (isEqual(state.gameId, action.payload.gameId)) {
                    state.messages.push(`Player ${action.payload.player.id} placed a mark on (${action.payload.x}, ${action.payload.y})`)
                }
            })
            .addCase(waitingForPlayerToPlay, (state: GameState, action) => {
                if (isEqual(state.gameId, action.payload.gameId)) {
                    state.turn = action.payload.playerId
                    state.timeout = new Date(Date.now() + action.payload.timeout)
                }
            })
            .addCase(boardUpdated, (state: GameState, action) => {
                if (isEqual(state.gameId, action.payload.gameId)) {
                    state.boardState = action.payload.board
                }
            })
            .addCase(gameEnded, (state: GameState, action) => {
                if (isEqual(state.gameId, action.payload.gameId)) {
                    state.stage = action.payload.result;
                    state.winner = action.payload.winner;
                    state.messages = [];
                    state.turn = null
                }
            })
            .addCase(acceptInvitation, (state: GameState, action) => {
                state.gameId = action.payload.game;
            })
            .addMatcher(createGameCommandPending, (state: GameState, action) => {
                state.gameId = action.meta.arg.originalArgs.gameId;
            })
    }
})

export const gameReducer = gameSlice.reducer
