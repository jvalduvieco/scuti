import {GameStage, GameState} from "../types";
import {BoardUpdated, CreateNewGame, GameEnded, GameStarted, PlaceMark, WaitingForPlayerPlay} from "../actions";

const initialGameState: GameState = {
  boardState: null,
  messages: [],
  stage: null,
  turn: null,
  winner: null,
  gameId: null,
  firstPlayer: null,
  secondPlayer: null
};

type GameActionTypes = CreateNewGame | GameStarted | BoardUpdated | WaitingForPlayerPlay | GameEnded | PlaceMark;

export const GameReducer = (state: GameState = initialGameState, action: GameActionTypes): GameState => {
  switch (action.type) {
    case "WAITING_FOR_PLAYER_PLAY":
      if (state.gameId?.id === action.payload.gameId.id) {
        return {...state, turn: action.payload.playerId}
      } else return state;
    case "PLACE_MARK":
      if (state.gameId?.id === action.payload.gameId.id) {
        return {
          ...state,
          messages: [...state.messages, `Player ${action.payload.player.id} placed a mark on (${action.payload.x}, ${action.payload.y})`]
        }
      } else return state;
    case "BOARD_UPDATED":
      if (state.gameId?.id === action.payload.gameId.id) {
        return {...state, boardState: action.payload.board}
      } else return state;
    case "CREATE_NEW_GAME":
      return {
        ...state,
        gameId: action.payload.gameId,
        firstPlayer: action.payload.firstPlayer,
        secondPlayer: action.payload.secondPlayer
      };
    case "GAME_STARTED":
      if (state.gameId?.id === action.payload.gameId.id) {
        return {
          ...state,
          boardState: action.payload.board,
          stage: (action.payload.stage as GameStage),
          gameId: action.payload.gameId
        }
      } else return state;
    case "GAME_ENDED":
      if (state.gameId?.id === action.payload.gameId.id) {
        return {...state, stage: action.payload.result, winner: action.payload.winner, messages: [], turn: null};
      } else return state;
    default:
      return state;
  }
}
