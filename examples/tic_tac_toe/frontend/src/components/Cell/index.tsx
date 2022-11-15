import {FC} from "react";
import {Button, Typography} from "@mui/material";
import {CellState, Handler, Id} from "../../types";
import {useGetUserQuery} from "../../backend/apiSlice";
import {Loading} from "../Loading";
import {useAppSelector} from "../../storeDefinition";
import isEqual from "lodash.isequal";

interface CellProps {
  owner: CellState
  onClick: Handler
}

export const Cell: FC<CellProps> = ({owner, onClick}: CellProps) => {
  const {
    isFetching,
    isLoading,
    isSuccess,
    isError,
    data: user
  } = useGetUserQuery(owner as Id, {skip: owner == null});
  const turn = useAppSelector(state => state.game.turn);
  const currentUserId = useAppSelector(state => state.client.currentUserId);
  // noinspection PointlessBooleanExpressionJS
  return <Button fullWidth variant="outlined"
                 disabled={owner !== null || (owner === null && isEqual(turn, currentUserId))} onClick={onClick}>
    {(isFetching || isLoading) && <Loading/>}
    {isError && <Typography>ERROR</Typography>}
    {isSuccess && owner !== null && user && <Typography>{user.alias}</Typography>}
    {owner === null && <Typography>Empty</Typography>}
  </Button>
}
