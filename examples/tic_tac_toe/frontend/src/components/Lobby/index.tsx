import {Button, Container, Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {ShowTopThreePlayers} from "../TopThreePlayers";
import {useNavigate} from "react-router";
import {useAppDispatch} from "../../storeDefinition";
import {useCreateUserMutation} from "../../backend/apiSlice";
import {createGameId, createPlayerId} from "../../tools/id";
import {createNewGame} from "../../actions";
import {AppRoutes} from "../../TicTacToeRoutes";
import {Id} from "../../types";

interface LobbyProps {
}

const aPlayer = (playerId: Id, alias: string = "default") => ({
  id: playerId,
  alias: alias,
  createdAt: new Date().toISOString()
});

export const Lobby: FC<LobbyProps> = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const [createUser] = useCreateUserMutation();

  const onNewGame = useCallback(async () => {
    const gameId = createGameId();
    const firstPlayerId = createPlayerId();
    const secondPlayerId = createPlayerId();

    await createUser(aPlayer(firstPlayerId)).unwrap();
    await createUser(aPlayer(secondPlayerId)).unwrap();
    dispatch(createNewGame({gameId, firstPlayer: firstPlayerId, secondPlayer: secondPlayerId}));
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
