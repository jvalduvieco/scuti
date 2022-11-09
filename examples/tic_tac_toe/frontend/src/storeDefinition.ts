import {
  AnyAction,
  combineReducers,
  configureStore,
  Middleware,
  PreloadedState,
  Store,
  ThunkDispatch
} from '@reduxjs/toolkit'
import {gameReducer} from "./slices/game";
import {TypedUseSelectorHook, useDispatch, useSelector} from "react-redux";
import {apiSlice} from './backend/apiSlice';

const rootReducer = combineReducers({
  game: gameReducer,
  [apiSlice.reducerPath]: apiSlice.reducer
});

export type AppState = ReturnType<typeof rootReducer>

export const setupStore = (preloadedState?: PreloadedState<AppState>, middlewaresBeforeDefault: Middleware[] = [], middlewaresAfterDefault: Middleware[] = []) =>
    configureStore({
      reducer: rootReducer,
      preloadedState,
      middleware: (getDefaultMiddleware) => [
        ...middlewaresBeforeDefault,
        ...getDefaultMiddleware(),
        ...middlewaresAfterDefault,
        apiSlice.middleware],
      devTools: process.env.NODE_ENV !== 'production',
    });

export type AppThunkDispatch = ThunkDispatch<AppState, any, AnyAction>;
export type AppStore = Omit<Store<AppState, AnyAction>, "dispatch"> & {
  dispatch: AppThunkDispatch;
};

export const useAppDispatch = () => useDispatch<AppThunkDispatch>();
export const useAppSelector: TypedUseSelectorHook<AppState> = useSelector;

