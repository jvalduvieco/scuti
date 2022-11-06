import {FC, useCallback} from "react";
import {Lobby} from "../components/Lobby";
import {AppRoutes} from "../TicTacToeRoutes";
import {createGameId, createPlayerId} from "../tools/id";
import {useNavigate} from "react-router";
import {createNewGame} from "../actions";
import {useAppDispatch} from "../store";

export const LobbyPage: FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const newGame = useCallback(() => {
    const gameId = createGameId();
    dispatch(createNewGame({gameId, firstPlayer: createPlayerId(), secondPlayer: createPlayerId()}));
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`);
  }, [dispatch, navigate]);
  return <Lobby onNewGame={newGame}/>
}
