import {Button, Container, Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {ShowTopThreePlayers} from "../TopThreePlayers";
import {useNavigate} from "react-router";
import {useAppDispatch} from "../../store";
import {useCreateUserMutation} from "../../backend/apiSlice";
import {createGameId, createPlayerId} from "../../tools/id";
import {createNewGame} from "../../actions";
import {AppRoutes} from "../../TicTacToeRoutes";

interface LobbyProps {
}

export const Lobby: FC<LobbyProps> = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [createUser] = useCreateUserMutation();

  const onNewGame = useCallback(async () => {
    const gameId = createGameId();
    const firstPlayer = createPlayerId();
    const secondPlayer = createPlayerId();
    await createUser(firstPlayer).unwrap();
    await createUser(secondPlayer).unwrap();
    dispatch(createNewGame({gameId, firstPlayer, secondPlayer}));
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`);
  }, [dispatch, navigate, createUser]);

  return <Container maxWidth="sm">
    <Grid container direction="column" alignContent="center" justifyContent="center" sx={{height: "100vh"}} spacing={3}>
      <Grid item>
        <Typography variant="h3">
          Welcome to tic tac toe!
        </Typography>
      </Grid>
      <Grid item>
        <ShowTopThreePlayers/>
      </Grid>
      <Grid item>
        <Button variant="contained" onClick={onNewGame} fullWidth>Play!</Button>
      </Grid>
    </Grid>
  </Container>
}
