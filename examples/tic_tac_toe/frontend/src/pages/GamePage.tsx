import {Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {connect} from "react-redux";
import {GameShow} from "../components/GameShow";
import {AppState, useAppDispatch} from "../storeDefinition";
import {createGameId} from "../tools/id";
import {CongratulationsPlayerWon} from "../components/CongratulationsPlayerWon";
import {AppRoutes} from "../TicTacToeRoutes";
import {Draw} from "../components/Draw";
import {useNavigate} from "react-router";
import {createGame, placeMark} from "../actions";
import {useJoinGameMutation} from "../backend/apiSlice";


const mapStateToProps = (state: AppState) => ({
  gameState: state.game
})
type GamePageProps = ReturnType<typeof mapStateToProps>;

const GamePage: FC<GamePageProps> = ({gameState}) => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [joinGame] = useJoinGameMutation();

  const onPlace = useCallback((x: number, y: number) => dispatch(placeMark({
        gameId: gameState.gameId!,
        player: gameState.turn!,
        x: x,
        y: y
      })),
      [dispatch, gameState.gameId, gameState.turn]);

  const onRestartGame = useCallback(async () => {
    const gameId = createGameId();
    dispatch(createGame({gameId, creator: gameState.firstPlayer!}));
    await joinGame({game: gameId, player: gameState.firstPlayer!})
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`)
  }, [dispatch, navigate, joinGame, gameState.firstPlayer]);

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


export default connect(mapStateToProps)(GamePage);
