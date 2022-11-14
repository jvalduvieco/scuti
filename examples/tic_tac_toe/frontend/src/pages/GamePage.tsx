import {Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {GameShow} from "../components/GameShow";
import {useAppSelector} from "../storeDefinition";
import {createGameId} from "../tools/id";
import {CongratulationsPlayerWon} from "../components/CongratulationsPlayerWon";
import {AppRoutes} from "../TicTacToeRoutes";
import {Draw} from "../components/Draw";
import {useNavigate} from "react-router";
import {
  useCreateGameMutation,
  useJoinGameMutation,
  usePlaceMarkMutation,
  useUserInvitedMutation
} from "../backend/apiSlice";

export const GamePage: FC = () => {
  const navigate = useNavigate();
  const [joinGame] = useJoinGameMutation();
  const [inviteUser] = useUserInvitedMutation();
  const [createGame] = useCreateGameMutation();
  const [placeMark] = usePlaceMarkMutation();
  const gameState = useAppSelector(state => state.game);
  const client = useAppSelector(state => state.client);

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
    const gameId = createGameId();
    await createGame({gameId, creator: client.currentUser!});
    await joinGame({game: gameId, player: client.currentUser!})
    await inviteUser({game: gameId, host: client.currentUser!, invited: client.opponent!})
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`)
  }, [client.currentUser, client.opponent, joinGame, inviteUser, navigate, createGame]);

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
    default:
      return <Grid container direction="row" justifyContent="center" sx={{height: "100vh"}} spacing={3}>
        <Grid item xs={8}>
          <GameShow gameState={gameState} onPlace={onPlace}/>
        </Grid>
      </Grid>
  }
}
