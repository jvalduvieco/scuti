import {call, put, takeEvery} from '@redux-saga/core/effects';
import {sagaErrorHandler} from '../tools/saga';
import {CreateNewGame, PlaceMark} from "../actions";
import TicTacToeBackendClient from "./TicTacToeBackendClient";
import {Action} from "redux";
import {Id} from "../types";

type Actions = CreateNewGame | PlaceMark;

function createInProgressAction(action: Action & { payload: { operationId: Id } }) {
  return {type: `REQUEST_IN_PROGRESS/${action.type}`, payload: {operationId: action.payload.operationId}};
}

function* doRequest(action: Actions) {
  switch (action.type) {
    case "CREATE_NEW_GAME":
      yield call(TicTacToeBackendClient.createNewGame,
          action.payload.gameId,
          action.payload.firstPlayer,
          action.payload.secondPlayer,
          action.payload.operationId);
      yield put(createInProgressAction(action))
      break;
    case "PLACE_MARK":
      yield call(TicTacToeBackendClient.placeMark,
          action.payload.gameId,
          action.payload.player,
          action.payload.x,
          action.payload.y,
          action.payload.operationId);
      yield put(createInProgressAction(action))
      break;
  }
}

export function* RequestsSaga() {
  yield takeEvery(["CREATE_NEW_GAME", "PLACE_MARK"], sagaErrorHandler(doRequest));
}
