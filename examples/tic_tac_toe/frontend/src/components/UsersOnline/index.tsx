import {FC, useCallback, useMemo} from "react";
import {Button, Grid, Paper, Typography} from "@mui/material";
import {useGetUserQuery, useGetUsersOnlineQuery} from "../../backend/apiSlice";
import {Loading} from "../Loading";
import {Id} from "../../types";
import {useDispatch, useSelector} from "react-redux";
import {choseOpponent} from "../../actions";
import {AppState} from "../../storeDefinition";

export const UserRow: FC<{ userId: Id }> = ({userId}) => {
  const {
    data,
    isLoading,
    isSuccess,
    isError,
    error,
    isFetching
  } = useGetUserQuery(userId);
  const dispatch = useDispatch();
  const opponent = useSelector((state: AppState) => state.client.opponent)

  const onChooseOpponent = useCallback(async () => {
    if (data) {
      dispatch(choseOpponent(data.user))
    }
  }, [dispatch, data])

  let content;

  if (isLoading || isFetching) {
    content = <Loading/>;
  } else if (isSuccess) {
    content = <Button fullWidth variant={data.user.id.id === opponent?.id.id?"contained":"outlined"} onClick={onChooseOpponent}>{data.user.alias}</Button>
  } else if (isError) {
    content = <Typography>An error occurred ({JSON.stringify(error)})</Typography>
  } else {
    throw Error();
  }
  return content;
}


export const UsersOnline: FC = () => {
  const {
    data: usersOnline,
    isLoading,
    isSuccess,
    isError,
    error,
    isFetching
  } = useGetUsersOnlineQuery();
  const currentUser = useSelector((state: AppState) => state.client.currentUser);

  const onlineUsersWithoutCurrentUser = useMemo(() => (usersOnline) ? usersOnline.onlineUsers.filter(u => u.id !== currentUser?.id.id) : [], [currentUser, usersOnline]);
  let content;
  if (isLoading || isFetching) {
    content = <Grid item><Loading/></Grid>;
  } else if (isSuccess) {
    content = onlineUsersWithoutCurrentUser.map((i, index) => <Grid item key={index}><UserRow userId={i}/></Grid>)
  } else if (isError) {
    content = <Grid item><Typography>An error occurred ({JSON.stringify(error)})</Typography></Grid>
  } else {
    throw Error();
  }
  return <Paper sx={{padding: 2, height: "300px", width: "100%"}}>
    <Typography variant="h4" align="center" gutterBottom>Online users</Typography>
    <Grid container direction="column" spacing={1} sx={{height: "260px"}}>
      {content}
    </Grid>
  </Paper>
}
