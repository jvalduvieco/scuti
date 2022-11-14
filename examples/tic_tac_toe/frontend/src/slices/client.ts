import {createSlice} from "@reduxjs/toolkit";
import {GameClientState} from "../types";
import {acceptInvitation, choseOpponent, userConnected} from "../actions";

const initialState: GameClientState = {
  currentUser: null,
  opponent: null
};

const gameClientSlice = createSlice({
  name: 'gameClient',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
        .addCase(userConnected, (state: GameClientState, action) => {
          state.currentUser = action.payload.id
        })
        .addCase(choseOpponent, (state: GameClientState, action) => {
          state.opponent = action.payload.id
        })
        .addCase(acceptInvitation, (state: GameClientState, action)=> {
          state.opponent = action.payload.host
        })
  }
})

export const gameClientReducer = gameClientSlice.reducer
