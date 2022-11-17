import {createSlice} from "@reduxjs/toolkit";
import {GameClientState} from "../types";
import {acceptInvitation, choseOpponent, userConnected} from "../actions";

const initialState: GameClientState = {
    currentUserId: null,
    opponentId: null
};

const gameClientSlice = createSlice({
    name: 'gameClient',
    initialState,
    reducers: {},
    extraReducers(builder) {
        builder
            .addCase(userConnected, (state: GameClientState, action) => {
                state.currentUserId = action.payload.id
            })
            .addCase(choseOpponent, (state: GameClientState, action) => {
                state.opponentId = action.payload.id
            })
            .addCase(acceptInvitation, (state: GameClientState, action) => {
                state.opponentId = action.payload.host
            })
    }
})

export const gameClientReducer = gameClientSlice.reducer
