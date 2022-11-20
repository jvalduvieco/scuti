import {push} from "@lagunovsky/redux-react-router";
import {addListener, createListenerMiddleware, TypedAddListener} from "@reduxjs/toolkit";
import {setupListeners} from "@reduxjs/toolkit/query";
import isEqual from "lodash.isequal";
import createSocketIoMiddleware from "redux-socket.io";
import io from "socket.io-client";
import {
  acceptInvitation,
  connectionStatusUpdated,
  createNewGame,
  topThreeListUpdated,
  userConnected,
  userInvited,
  UsersOnlineUpdated
} from "./actions";
import {apiSlice} from "./backend/apiSlice";
import {BACKEND_URL} from "./config";
import {AppStartListening, AppState, AppThunkDispatch, setupStore} from "./storeDefinition";
import {AppRoutes} from "./TicTacToeRoutes";


const buildSocketIoMiddleware = () => {
  const socket = io(BACKEND_URL);
  const socketIoMiddleware = createSocketIoMiddleware(socket, "server/");
  socket.on("connect", (socket: { id: string; }) => store.dispatch(connectionStatusUpdated({
    newStatus: "Online",
    sid: socket.id
  })));
  socket.on("reconnect", (socket: { id: string; }) => store.dispatch(connectionStatusUpdated({
    newStatus: "Online",
    sid: socket.id
  })));
  socket.on("disconnect", (socket: { id: string; }) => store.dispatch(connectionStatusUpdated({
    newStatus: "Offline",
    sid: socket.id
  })));
  return socketIoMiddleware;
}

export const listenerMiddleware = createListenerMiddleware();

export const startAppListening =
    listenerMiddleware.startListening as AppStartListening


export const addAppListener = addListener as TypedAddListener<AppState,
    AppThunkDispatch>

export const store = setupStore(undefined, [listenerMiddleware.middleware], [buildSocketIoMiddleware()]);

setupListeners(store.dispatch);

startAppListening({
  actionCreator: topThreeListUpdated,
  effect: async (action, {dispatch}) => {
    await dispatch(apiSlice.util.invalidateTags(["TopThreeList"]))
  }
})

startAppListening({
  actionCreator: UsersOnlineUpdated,
  effect: async (action, {dispatch}) => {
    await dispatch(apiSlice.util.invalidateTags(["UsersOnline"]))
  }
})

startAppListening({
  actionCreator: userConnected,
  effect: async (action, {dispatch}) => {
    dispatch({type: "server/ASSOCIATE_USER_TO_SESSION", data: {userId: action.payload.id}})
    await dispatch(apiSlice.endpoints.userConnected.initiate(action.payload.id));
  }
})

startAppListening({
  actionCreator: userInvited,
  effect: async (action, {dispatch, getState}) => {
    const state = await getState();
    if (isEqual(state.client.currentUserId, action.payload.invited)) {
      await dispatch(acceptInvitation({...action.payload}))
    }
  }
})

startAppListening({
  actionCreator: acceptInvitation,
  effect: async (action, {dispatch, getState}) => {
    const state = await getState();
    if (isEqual(state.client.currentUserId, action.payload.invited)) {
      await dispatch(apiSlice.endpoints.joinGame.initiate({
        player: action.payload.invited,
        game: action.payload.game
      }));
      await dispatch(push(`${AppRoutes.GAME_SCREEN}/${action.payload.game.id}`))
    }
  }
})

startAppListening({
  actionCreator: createNewGame,
  effect: async ({payload: {gameId, creatorId, opponentId}}, {dispatch}) => {
    await dispatch(apiSlice.endpoints.createGame.initiate({gameId, creator: creatorId}));
    await dispatch(apiSlice.endpoints.userInvited.initiate({host: creatorId, invited: opponentId, game: gameId}));
    await dispatch(apiSlice.endpoints.joinGame.initiate({game: gameId, player: creatorId}));
    await dispatch(push(`${AppRoutes.GAME_SCREEN}/${gameId.id}`));

  }
})
