import createSagaMiddleware from "redux-saga";
import {BACKEND_URL} from "./config";
import io from 'socket.io-client';
import createSocketIoMiddleware from "redux-socket.io";
import {applyMiddleware, combineReducers, compose, createStore, Reducer} from "redux";
import {createReduxHistoryContext} from "redux-first-history";
import {createHashHistory} from "history";
import {connectionStatusUpdated} from "./actions";
import {GameReducer} from "./reducers/game";
import {RequestsSaga} from "./backend/RequestsSaga";

const {createReduxHistory, routerMiddleware, routerReducer} = createReduxHistoryContext({
  history: createHashHistory(),
});
const rootReducer: Reducer = combineReducers({
  router: routerReducer,
  game: GameReducer,
});

const composeEnhancers = ((window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ &&
    (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({trace: true, traceLimit: 25})) || compose;

const configureStore = (rootReducer: Reducer) => {
  const sagaMiddleware = createSagaMiddleware();

  const socket = io(BACKEND_URL);
  const socketIoMiddleware = createSocketIoMiddleware(socket, "server/");
  socket.on("connect", () => store.dispatch(connectionStatusUpdated("Online")));
  socket.on("disconnect", () => store.dispatch(connectionStatusUpdated("Offline")));

  const middlewares = [
    applyMiddleware(socketIoMiddleware),
    applyMiddleware(sagaMiddleware),
    applyMiddleware(routerMiddleware),
  ];

  const store = createStore(
      rootReducer,
      composeEnhancers(...middlewares)
  );
  sagaMiddleware.run(RequestsSaga);
  return store;
};
export const store = configureStore(rootReducer);
export const appHistory = createReduxHistory(store);
export type AppState = ReturnType<typeof rootReducer>;
