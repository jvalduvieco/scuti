import {FC, useCallback} from "react";
import {Lobby} from "../components/Lobby";
import {useDispatch} from "react-redux";
import {createNewGame} from "../actions";
import {push} from "redux-first-history";
import {AppRoutes} from "../TicTacToeRoutes";
import {createGameId, createOperationId, createPlayerId} from "../tools/id";

export const LobbyPage: FC = () => {
  const dispatch = useDispatch();
  const newGame = useCallback(() => {
    const gameId = createGameId();
    dispatch(createNewGame(gameId, createPlayerId(), createPlayerId(), createOperationId()));
    dispatch(push(`${AppRoutes.GAME_SCREEN}/${gameId.id}`));
  }, [dispatch]);
  return <Lobby onNewGame={newGame}/>
}
