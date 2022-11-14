import {FC, useCallback, useMemo} from "react";
import {Button, Grid, Paper, Typography} from "@mui/material";
import {useGetUserQuery, useGetUsersOnlineQuery} from "../../backend/apiSlice";
import {Id} from "../../types";
import {choseOpponent} from "../../actions";
import {useAppDispatch, useAppSelector} from "../../storeDefinition";
import {RenderOnSuccess} from "../RenderOnSuccess";

export const UserRow: FC<{ userId: Id }> = ({userId}) => {
  const {
    data: user,
    ...status
  } = useGetUserQuery(userId);
  const dispatch = useAppDispatch();
  const opponent = useAppSelector(state => state.client.opponent)

  const onChooseOpponent = useCallback(async () => {
    if (user) {
      dispatch(choseOpponent(user))
    }
  }, [dispatch, user])

  return <RenderOnSuccess queryStatus={status} mustBeDefined={user}>
    <>{user && <Button fullWidth variant={user.id.id === opponent?.id ? "contained" : "outlined"}
                       onClick={onChooseOpponent}>{user.alias}</Button>}</>
  </RenderOnSuccess>
}


export const UsersOnline: FC = () => {
  const {
    data: usersOnline,
    ...status
  } = useGetUsersOnlineQuery();
  const currentUser = useAppSelector(state => state.client.currentUser);

  const onlineUsersWithoutCurrentUser = useMemo(() => (usersOnline) ? usersOnline.filter(u => u.id !== currentUser?.id) : [], [currentUser, usersOnline]);

  return <RenderOnSuccess queryStatus={status} mustBeDefined={usersOnline}>
    <Paper sx={{padding: 2, height: "300px", width: "100%"}}>
      <Typography variant="h4" align="center" gutterBottom>Online users</Typography>
      <Grid container direction="column" spacing={1} sx={{height: "260px"}}>
        {onlineUsersWithoutCurrentUser.map((i, index) => <Grid item key={index}><UserRow userId={i}/></Grid>)}
      </Grid>
    </Paper>
  </RenderOnSuccess>
}
