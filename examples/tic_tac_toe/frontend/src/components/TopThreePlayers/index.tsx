import {Divider, Grid, Paper, Typography} from "@mui/material";
import {useGetTopThreePlayersQuery, useGetUserQuery} from "../../backend/apiSlice";
import {Id, ScoreListItem} from "../../types";
import {FC} from "react";

const ScoreListItemShow: FC<{ id: Id, score: number, position: number }> = ({id, score, position}) => {
  const {
    data: user,
      ...restGetUser
  } = useGetUserQuery(id as Id);

  return <Grid item container direction="row">
    <Grid item xs={1}>
      {position === 1 && "🏆"}
      {position === 2 && "🏅"}
      {position === 3 && "🍫"}
    </Grid>
    <Grid item xs><Typography variant="body1" align="center">{user?.alias}</Typography></Grid>
    <Grid item xs><Typography variant="body1" align="center">{score}</Typography></Grid>
  </Grid>
};

export const ShowTopThreePlayers = () => {
  const {
    data: topThreeList,
    isLoading,
    isSuccess,
    isError,
    error,
    isFetching
  } = useGetTopThreePlayersQuery()

  let content;
  if (isLoading || isFetching) {
    content = <Typography>Loading...</Typography>
  } else if (isSuccess && topThreeList) {
    content = <Paper sx={{padding: 1}}>
      <Typography variant="h4" align="center">⚡ ⭐ 🏆 Hall of fame 🏆 ⭐ ⚡</Typography>
      <Divider variant="middle" sx={{marginBottom: 1}}/>
      <Grid container direction="column" spacing={1}>
        {topThreeList.map((item: ScoreListItem, index: number) =>
            <ScoreListItemShow key={index} id={item.id} score={item.score} position={index + 1}/>)}
        {topThreeList.length === 0 && <Typography variant="h6" align="center" sx={{padding:2}}>No winners yet! Be the first!</Typography>}
      </Grid>
    </Paper>
  } else if (isError) {
    content = <Typography>An error occurred loading top three player list. {error.toString()}</Typography>
  }
  return <>{content}</>
}
