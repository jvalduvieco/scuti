import {Grid, Typography} from "@mui/material";
import {useGetTopThreePlayersQuery} from "../../backend/apiSlice";
import {createOperationId} from "../../tools/id";

export const ShowTopThreePlayers = () => {
  const {
    status,
    data: topThreeList = [],
    isLoading,
    isSuccess,
    isError,
    error,
    isFetching
  } = useGetTopThreePlayersQuery(createOperationId())
  console.log(status, isLoading, isSuccess, isError, isFetching, topThreeList)

  let content;
  if (isLoading) {
    content = <Typography>Loading...</Typography>
  } else if (isSuccess) {
    content = <Grid container direction="column">
      {topThreeList.map((item: string, index: number) => <Grid item key={index}>{item}</Grid>)}
    </Grid>
  }
  if (isError) {
    content = <Typography>An error occurred loading top three player list. {error.toString()}</Typography>
  }
  return <>{content}</>
}
