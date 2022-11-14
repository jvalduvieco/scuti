import {Button, Container, Grid, Typography} from "@mui/material";
import {FC, useCallback} from "react";
import {ShowTopThreePlayers} from "../TopThreePlayers";
import {useAppSelector} from "../../storeDefinition";
import {useGetUserQuery} from "../../backend/apiSlice";
import UserForm from "../UserForm";
import {UserShow} from "../UserShow";
import {UsersOnline} from "../UsersOnline";
import {Id} from "../../types";
import {RenderOnSuccess} from "../RenderOnSuccess";
import {createNewGame} from "../../actions";
import {useDispatch} from "react-redux";
import {createGameId} from "../../tools/id";

export const Lobby: FC = () => {
  const dispatch = useDispatch();
  const currentUserId = useAppSelector(state => state.client.currentUser);
  const opponentId = useAppSelector(state => state.client.opponent);

  const {
    data: currentUser,
    ...currentUserQueryStatus
  } = useGetUserQuery(currentUserId as Id, {skip: currentUserId === null});

  const onNewGame = useCallback(async () => {
    if (currentUserId !== null && opponentId !== null) {
      dispatch(createNewGame({gameId: createGameId(), creatorId: currentUserId, opponentId}));
    }
  }, [dispatch, currentUserId, opponentId]);

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
          <RenderOnSuccess queryStatus={[currentUserQueryStatus]} mustBeDefined={[currentUser]}>
            {(currentUser && <UserShow alias={currentUser.alias}/>) || <></>}
          </RenderOnSuccess>
        </Grid>
        <Grid item xs={6}>
          <UsersOnline/>
        </Grid>
      </Grid>

      <Grid item>
        <ShowTopThreePlayers/>
      </Grid>
      <Grid item>
        <Button variant="contained" onClick={onNewGame} fullWidth
                disabled={!(currentUserId && opponentId)}>Play!</Button>
      </Grid>
    </Grid>
  </Container>
}
