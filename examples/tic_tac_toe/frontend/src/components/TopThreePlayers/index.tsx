import {Divider, Grid, Paper, Typography} from "@mui/material";
import {useGetTopThreePlayersQuery, useGetUserQuery} from "../../backend/apiSlice";
import {Id, ScoreListItem} from "../../types";
import {FC} from "react";
import {RenderOnSuccess} from "../RenderOnSuccess";

const ScoreListItemShow: FC<{ id: Id, score: number, position: number }> = ({id, score, position}) => {
  const {
    data: user,
    ...status
  } = useGetUserQuery(id as Id);

  return <RenderOnSuccess queryStatus={status} mustBeDefined={user}>
    <Grid item container direction="row">
      <Grid item xs={1}>
        {position === 1 && "🏆"}
        {position === 2 && "🏅"}
        {position === 3 && "🍫"}
      </Grid>
      <Grid item xs><Typography variant="body1" align="center">{user?.alias}</Typography></Grid>
      <Grid item xs><Typography variant="body1" align="center">{score}</Typography></Grid>
    </Grid>
  </RenderOnSuccess>
};

export const ShowTopThreePlayers = () => {
  const {data: topThreeList = [], ...status} = useGetTopThreePlayersQuery()

  return <RenderOnSuccess queryStatus={status} mustBeDefined={topThreeList}>
    <Paper sx={{padding: 1}}>
      <Typography variant="h4" align="center">⚡ ⭐ 🏆 Hall of fame 🏆 ⭐ ⚡</Typography>
      <Divider variant="middle" sx={{marginBottom: 1}}/>
      <Grid container direction="column" spacing={1}>
        {topThreeList.map((item: ScoreListItem, index: number) =>
            <ScoreListItemShow key={index} id={item.id} score={item.score} position={index + 1}/>)}
        {topThreeList.length === 0 &&
            <Typography variant="h6" align="center" sx={{padding: 2}}>No winners yet! Be the first!</Typography>}
      </Grid>
    </Paper>
  </RenderOnSuccess>
}
