import {createEntityAdapter, createSlice} from "@reduxjs/toolkit";
import {userFetched} from "../backend/apiSlice";
import {userConnected} from "../actions";

const usersAdapter = createEntityAdapter()

const initialState = usersAdapter.getInitialState()

const usersSlice = createSlice({
  name: 'usersSlice',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
        .addCase(userConnected,
            (state, action) => usersAdapter.upsertOne(state, action.payload))
        .addMatcher(userFetched,
            (state, action) => usersAdapter.upsertOne(state, action.payload.user));
  }
})

export const userReducer = usersSlice.reducer
