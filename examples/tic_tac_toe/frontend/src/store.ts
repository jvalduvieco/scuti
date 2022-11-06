import {AnyAction, configureStore, Store, ThunkDispatch} from '@reduxjs/toolkit'
import {BACKEND_URL} from "./config";
import io from 'socket.io-client';
import createSocketIoMiddleware from "redux-socket.io";
import {connectionStatusUpdated} from "./actions";
import {gameReducer} from "./slices/game";
import {TypedUseSelectorHook, useDispatch, useSelector} from "react-redux";

const socket = io(BACKEND_URL);
const socketIoMiddleware = createSocketIoMiddleware(socket, "server/");
socket.on("connect", () => store.dispatch(connectionStatusUpdated({newStatus: "Online"})));
socket.on("disconnect", () => store.dispatch(connectionStatusUpdated({newStatus: "Offline"})));

export const store = configureStore({
  reducer: {
    game: gameReducer,
  },
  middleware: (getDefaultMiddleware) => [...getDefaultMiddleware(), socketIoMiddleware],
  devTools: process.env.NODE_ENV !== 'production',
});

export type AppState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export type AppThunkDispatch = ThunkDispatch<AppState, any, AnyAction>;
export type AppStore = Omit<Store<AppState, AnyAction>, "dispatch"> & {
  dispatch: AppThunkDispatch;
};

export const useAppDispatch = () => useDispatch<AppThunkDispatch>();
export const useAppSelector: TypedUseSelectorHook<AppState> = useSelector;

