import {setupListeners} from "@reduxjs/toolkit/query";
import {connectionStatusUpdated, topThreeListUpdated} from "./actions";
import {apiSlice} from "./backend/apiSlice";
import io from "socket.io-client";
import {BACKEND_URL} from "./config";
import createSocketIoMiddleware from "redux-socket.io";
import {setupStore} from "./storeDefinition";
import {createListenerMiddleware} from "@reduxjs/toolkit";


const buildSocketIoMiddleware = () => {
  const socket = io(BACKEND_URL);
  const socketIoMiddleware = createSocketIoMiddleware(socket, "server/");
  socket.on("connect", () => store.dispatch(connectionStatusUpdated({newStatus: "Online"})));
  socket.on("disconnect", () => store.dispatch(connectionStatusUpdated({newStatus: "Offline"})));
  return socketIoMiddleware;
}

const listenerMiddleware = createListenerMiddleware();
export const store = setupStore(undefined, [listenerMiddleware.middleware], [buildSocketIoMiddleware()]);

setupListeners(store.dispatch);

listenerMiddleware.startListening({
  actionCreator: topThreeListUpdated,
  effect: async (action, {dispatch}) => {
    dispatch(apiSlice.util.invalidateTags(["TopThreeList"]))
  }
})
