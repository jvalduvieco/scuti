import {Grid, Typography} from "@mui/material";
import {useGetTopThreePlayersQuery} from "../../backend/apiSlice";
import {Id, ScoreListItem} from "../../types";
import {FC} from "react";

const ScoreListItemShow: FC<{ id: Id, score: number }> = ({id, score}) => <Grid item>
  {`${id.id} - ${score}`}
</Grid>;

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
    content = <Grid container direction="column">
      {topThreeList.list.map((item: ScoreListItem, index: number) =>
          <ScoreListItemShow key={index} id={item.id} score={item.score}/>)}
    </Grid>
  } else if (isError) {
    content = <Typography>An error occurred loading top three player list. {error.toString()}</Typography>
  }
  return <>{content}</>
}
