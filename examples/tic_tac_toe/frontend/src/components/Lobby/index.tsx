import {Button, Container, Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {ShowTopThreePlayers} from "../TopThreePlayers";
import {useNavigate} from "react-router";
import {AppState, useAppDispatch} from "../../storeDefinition";
import {useJoinGameMutation, useUserInvitedMutation} from "../../backend/apiSlice";
import {createGameId} from "../../tools/id";
import {createGame} from "../../actions";
import {AppRoutes} from "../../TicTacToeRoutes";
import {Id} from "../../types";
import UserForm from "../UserForm";
import {useSelector} from "react-redux";
import {UserShow} from "../UserShow";
import {UsersOnline} from "../UsersOnline";

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
  const [inviteUser] = useUserInvitedMutation();
  const [joinGame] = useJoinGameMutation();
  const currentUser = useSelector((state: AppState) => state.client.currentUser);
  const opponent = useSelector((state: AppState) => state.client.opponent);

  const onNewGame = useCallback(async () => {
    if (!currentUser || !opponent) throw Error("currentUser can not be null")
    const gameId = createGameId();
    const firstPlayerId = currentUser.id;
    dispatch(createGame({gameId, creator: firstPlayerId}));
    await inviteUser({host: firstPlayerId, invited: opponent.id, game: gameId});
    await joinGame({game: gameId, player: firstPlayerId})
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`);
  }, [dispatch, navigate, inviteUser, joinGame, currentUser, opponent]);

  return <Container maxWidth="sm">
    <Grid container direction="column" alignContent="center" justifyContent="center" sx={{height: "100vh"}} spacing={3}>
      <Grid item>
        <Typography variant="h3">
          Welcome to tic tac toe!
        </Typography>
      </Grid>
      <Grid item container direction="row" spacing={2}>
        <Grid item xs={6}>
          {!currentUser && <UserForm/>}
          {currentUser && <UserShow alias={currentUser.alias}/>}
        </Grid>
        <Grid item xs={6}>
          <UsersOnline/>
        </Grid>
      </Grid>

      <Grid item>
        <ShowTopThreePlayers/>
      </Grid>
      <Grid item>
        <Button variant="contained" onClick={onNewGame} fullWidth disabled={!(currentUser && opponent)}>Play!</Button>
      </Grid>
    </Grid>
  </Container>
}
