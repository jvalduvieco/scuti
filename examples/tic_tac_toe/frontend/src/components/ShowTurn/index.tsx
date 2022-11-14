import {FC} from "react";
import {Paper, Typography} from "@mui/material";
import {Id} from "../../types";
import {useGetUserQuery} from "../../backend/apiSlice";

interface GameStageProps {
  turn: Id | null
}

export const ShowTurn: FC<GameStageProps> = ({turn}: GameStageProps) => {
  const {
    data: user,
    ...restGetUser
  } = useGetUserQuery(turn as Id);
  return <Paper sx={{padding: 1, width: "100%"}}>
    <Typography align="center">
      It's {user?.alias} turn
    </Typography>
  </Paper>
}
