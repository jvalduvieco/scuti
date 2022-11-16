import {Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {GameShow} from "../components/GameShow";
import {useAppSelector} from "../storeDefinition";
import {createGameId} from "../tools/id";
import {CongratulationsPlayerWon} from "../components/CongratulationsPlayerWon";
import {AppRoutes} from "../TicTacToeRoutes";
import {Draw} from "../components/Draw";
import {useNavigate} from "react-router";
import {usePlaceMarkMutation} from "../backend/apiSlice";
import {createNewGame} from "../actions";
import {useDispatch} from "react-redux";
import {GameAborted} from "../components/GameAborted";

export const GamePage: FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [placeMark] = usePlaceMarkMutation();
  const gameState = useAppSelector(state => state.game);
  const {currentUserId, opponentId} = useAppSelector(state => state.client);

  const onPlace = useCallback(async (x: number, y: number) =>
              await placeMark({
                gameId: gameState.gameId!,
                player: gameState.turn!,
                x: x,
                y: y
              }),
          [placeMark, gameState.gameId, gameState.turn]
      )
  ;

  const onRestartGame = useCallback(async () => {
    if (currentUserId !== null && opponentId !== null) {
      await dispatch(createNewGame({gameId: createGameId(), creatorId: currentUserId, opponentId}));
    }
  }, [dispatch, currentUserId, opponentId]);

  const onGotoLobby = useCallback(() => navigate(AppRoutes.HOME), [navigate])
  switch (gameState.stage) {
    case null:
      return <Typography>Loading</Typography>
    case "WAITING_FOR_PLAYERS":
      return <Typography>Waiting for players</Typography>
    case "DRAW":
      return <Draw gotoLobby={onGotoLobby} restartGame={onRestartGame}/>
    case "PLAYER_WON":
      return <CongratulationsPlayerWon winner={gameState.winner!}
                                       gotoLobby={onGotoLobby}
                                       restartGame={onRestartGame}/>
    case "GAME_ABORTED":
      return <GameAborted gotoLobby={onGotoLobby} restartGame={onRestartGame}/>
    default:
      return <Grid container direction="row" justifyContent="center" sx={{height: "100vh"}} spacing={3}>
        <Grid item xs={8}>
          <GameShow gameState={gameState} onPlace={onPlace}/>
        </Grid>
      </Grid>
  }
}
