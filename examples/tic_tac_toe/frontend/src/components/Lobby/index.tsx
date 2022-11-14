import {Button, Container, Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {ShowTopThreePlayers} from "../TopThreePlayers";
import {useNavigate} from "react-router";
import {useAppSelector} from "../../storeDefinition";
import {
  useCreateGameMutation,
  useGetUserQuery,
  useJoinGameMutation,
  useUserInvitedMutation
} from "../../backend/apiSlice";
import {createGameId} from "../../tools/id";
import {AppRoutes} from "../../TicTacToeRoutes";
import UserForm from "../UserForm";
import {UserShow} from "../UserShow";
import {UsersOnline} from "../UsersOnline";
import {Id} from "../../types";

export const Lobby: FC = () => {
  const navigate = useNavigate();
  const [inviteUser] = useUserInvitedMutation();
  const [createGame] = useCreateGameMutation();
  const [joinGame] = useJoinGameMutation();
  const currentUserId = useAppSelector(state => state.client.currentUser);
  const opponentId = useAppSelector(state => state.client.opponent);

  const {
    data: currentUser,
    ...restCurrentUserQuery
  } = useGetUserQuery(currentUserId as Id, {skip: currentUserId === null});

  const {
    data: opponent,
    ...restOpponentQuery
  } = useGetUserQuery(opponentId as Id, {skip: opponentId === null});

  const onNewGame = useCallback(async () => {
    if (!currentUserId || !opponentId) throw Error("currentUserId or opponentId can not be null")
    const gameId = createGameId();
    await createGame({gameId, creator: currentUserId});
    await inviteUser({host: currentUserId, invited: opponentId, game: gameId});
    await joinGame({game: gameId, player: currentUserId})
    navigate(`${AppRoutes.GAME_SCREEN}/${gameId.id}`);
  }, [currentUserId, opponentId, createGame, inviteUser, joinGame, navigate]);

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
