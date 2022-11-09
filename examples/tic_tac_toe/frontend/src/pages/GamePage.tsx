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
import {createNewGame, placeMark} from "../actions";


const mapStateToProps = (state: AppState) => ({
  gameState: state.game
})
type GamePageProps = ReturnType<typeof mapStateToProps>;

const GamePage: FC<GamePageProps> = ({gameState}) => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const onPlace = useCallback((x: number, y: number) => dispatch(placeMark({
        gameId: gameState.gameId!,
        player: gameState.turn!,
        x: x,
        y: y
      })),
      [dispatch, gameState.gameId, gameState.turn]);

  const onRestartGame = useCallback(() => {
    const gameId = createGameId();
    dispatch(createNewGame({gameId, firstPlayer: gameState.firstPlayer!, secondPlayer: gameState.secondPlayer!}));
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`)
  }, [dispatch, navigate, gameState.firstPlayer, gameState.secondPlayer]);

  const onGotoLobby = useCallback(() => navigate(AppRoutes.HOME), [navigate])
  switch (gameState.stage) {
    case null:
      return <Typography>Loading</Typography>
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
