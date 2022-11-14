import {FC} from "react";
import {Paper, Typography} from "@mui/material";
import {Id} from "../../types";
import {useGetUserQuery} from "../../backend/apiSlice";
import {RenderOnSuccess} from "../RenderOnSuccess";

interface GameStageProps {
  turn: Id | null
}

export const ShowTurn: FC<GameStageProps> = ({turn}: GameStageProps) => {
  const {
    data: user,
    ...status
  } = useGetUserQuery(turn as Id);
  return <RenderOnSuccess queryStatus={status} mustBeDefined={user}>
    <Paper sx={{padding: 1, width: "100%"}}>
      <Typography align="center">
        It's {user?.alias} turn
      </Typography>
    </Paper>
  </RenderOnSuccess>
}
