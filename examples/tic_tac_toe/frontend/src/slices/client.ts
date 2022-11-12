import {createSlice} from "@reduxjs/toolkit";
import {GameClientState} from "../types";
import {choseOpponent, userConnected} from "../actions";

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
          state.currentUser = action.payload
        })
        .addCase(choseOpponent, (state: GameClientState, action) => {
          state.opponent = action.payload
        })
  }
})

export const gameClientReducer = gameClientSlice.reducer
