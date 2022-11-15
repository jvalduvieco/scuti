import {
  AnyAction,
  combineReducers,
  configureStore,
  Middleware,
  PreloadedState,
  Store,
  ThunkDispatch, TypedStartListening
} from "@reduxjs/toolkit"
import {gameReducer} from "./slices/game";
import {TypedUseSelectorHook, useDispatch, useSelector} from "react-redux";
import {apiSlice} from "./backend/apiSlice";
import {gameClientReducer} from "./slices/client";
import {userReducer} from "./slices/users";
import {createBrowserHistory} from "history";
import {createRouterMiddleware, createRouterReducerMapObject} from "@lagunovsky/redux-react-router";

export const appHistory = createBrowserHistory()
const routerMiddleware = createRouterMiddleware(appHistory)


const rootReducer = combineReducers({
  game: gameReducer,
  client: gameClientReducer,
  user: userReducer,
  ...createRouterReducerMapObject(appHistory),
  [apiSlice.reducerPath]: apiSlice.reducer
});

export type AppState = ReturnType<typeof rootReducer>

export const setupStore = (preloadedState?: PreloadedState<AppState>, middlewaresBeforeDefault: Middleware[] = [], middlewaresAfterDefault: Middleware[] = []) =>
    configureStore({
      reducer: rootReducer,
      preloadedState,
      middleware: (getDefaultMiddleware) => [
        routerMiddleware,
        ...middlewaresBeforeDefault,
        ...getDefaultMiddleware(),
        ...middlewaresAfterDefault,
        apiSlice.middleware],
      devTools: process.env.NODE_ENV !== "production",
    });

export type AppThunkDispatch = ThunkDispatch<AppState, any, AnyAction>;
export type AppStore = Omit<Store<AppState, AnyAction>, "dispatch"> & {
  dispatch: AppThunkDispatch;
};

export type AppStartListening = TypedStartListening<AppState, AppThunkDispatch>

export const useAppDispatch = () => useDispatch<AppThunkDispatch>();
export const useAppSelector: TypedUseSelectorHook<AppState> = useSelector;

