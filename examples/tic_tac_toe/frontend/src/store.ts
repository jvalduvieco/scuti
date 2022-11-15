import {setupListeners} from "@reduxjs/toolkit/query";
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
import io from "socket.io-client";
import {BACKEND_URL} from "./config";
import createSocketIoMiddleware from "redux-socket.io";
import {AppStartListening, AppState, AppThunkDispatch, setupStore} from "./storeDefinition";
import {addListener, createListenerMiddleware, TypedAddListener} from "@reduxjs/toolkit";
import {push} from "@lagunovsky/redux-react-router";
import {AppRoutes} from "./TicTacToeRoutes";


const buildSocketIoMiddleware = () => {
  const socket = io(BACKEND_URL);
  const socketIoMiddleware = createSocketIoMiddleware(socket, "server/");
  socket.on("connect", () => store.dispatch(connectionStatusUpdated({newStatus: "Online"})));
  socket.on("disconnect", () => store.dispatch(connectionStatusUpdated({newStatus: "Offline"})));
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
    await dispatch(apiSlice.endpoints.userConnected.initiate(action.payload.id));
  }
})

startAppListening({
  actionCreator: userInvited,
  effect: async (action, {dispatch, getState}) => {
    const state = await getState();
    if (state.client.currentUserId?.id === action.payload.invited.id) {
      await dispatch(acceptInvitation({...action.payload}))
    }
  }
})

startAppListening({
  actionCreator: acceptInvitation,
  effect: async (action, {dispatch, getState}) => {
    const state = await getState();
    if (state.client.currentUserId?.id === action.payload.invited.id) {
      await dispatch(apiSlice.endpoints.joinGame.initiate({player: action.payload.invited, game: action.payload.game}));
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
