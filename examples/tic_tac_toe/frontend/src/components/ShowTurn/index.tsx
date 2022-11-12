import {FC} from "react";
import {Paper, styled, Typography} from "@mui/material";
import {GameStage, Id} from "../../types";
import {useGetUserQuery} from "../../backend/apiSlice";

interface GameStageProps {
  turn: Id | null
}

export const ShowTurn: FC<GameStageProps> = ({turn}: GameStageProps) => {
  const {
    isFetching,
    isLoading,
    isSuccess,
    isError,
    data: user
  } = useGetUserQuery(turn as Id);
  return <Paper sx={{padding: 1, width: "100%"}}>
    <Typography align="center">
      It's {user?.user.alias} turn
    </Typography>
  </Paper>
}
