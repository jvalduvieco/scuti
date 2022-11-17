import {FC} from "react";
import {Paper, Typography} from "@mui/material";
import {Id} from "../../types";
import {useGetUserQuery} from "../../backend/apiSlice";
import {RenderOnSuccess} from "../RenderOnSuccess";
import {useCountdown} from "../useCountDown";

interface ShowTurnProps {
    turn: Id
    timeout: Date
}

export const ShowTurn: FC<ShowTurnProps> = ({turn, timeout}: ShowTurnProps) => {
    const {
        data: user,
        ...status
    } = useGetUserQuery(turn as Id, {skip: turn === null});
    const {seconds} = useCountdown(timeout);

    return <RenderOnSuccess queryStatus={status} mustBeDefined={[user, timeout]}>
        <Paper sx={{padding: 1, width: "100%"}}>
            <Typography align="center">
                It's {user?.alias} turn
            </Typography>
            <Typography align="center">
                {seconds} s
            </Typography>
        </Paper>
    </RenderOnSuccess>
}
