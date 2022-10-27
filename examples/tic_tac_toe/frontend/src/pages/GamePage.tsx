import {Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {connect, useDispatch} from "react-redux";
import {GameShow} from "../components/GameShow";
import {AppState} from "../store";
import {createNewGame, placeMark} from "../actions";
import {createGameId, createOperationId} from "../tools/id";
import {CongratulationsPlayerWon} from "../components/CongratulationsPlayerWon";
import {push} from "redux-first-history";
import {AppRoutes} from "../TicTacToeRoutes";
import {Draw} from "../components/Draw";


const mapStateToProps = (state: AppState) => ({
  gameState: state.game
})
type GamePageProps = ReturnType<typeof mapStateToProps>;

const GamePage: FC<GamePageProps> = ({gameState}) => {
  const dispatch = useDispatch();
  const onPlace = useCallback((x: number, y: number) =>
          dispatch(
              placeMark(gameState.gameId, gameState.turn, x, y, createOperationId())),
      [dispatch, gameState.gameId, gameState.turn]);
  const onRestartGame = useCallback(() => {
    const gameId = createGameId();
    dispatch(createNewGame(gameId, gameState.firstPlayer, gameState.secondPlayer, createOperationId()));
    dispatch(push(`${AppRoutes.GAME_SCREEN}/${gameId.id}`))
  }, [dispatch, gameState.firstPlayer, gameState.secondPlayer]);
  const onGotoLobby = useCallback(() => dispatch(push(AppRoutes.HOME)), [dispatch])
  switch (gameState.stage) {
    case null:
      return <Typography>Loading</Typography>
    case "DRAW":
      return <Draw gotoLobby={onGotoLobby} restartGame={onRestartGame}/>
    case "PLAYER_WON":
      return <CongratulationsPlayerWon winner={gameState.winner}
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
