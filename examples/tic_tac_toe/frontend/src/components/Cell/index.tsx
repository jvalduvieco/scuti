import {FC} from "react";
import {Button, Typography} from "@mui/material";
import {CellState, Handler, Id} from "../../types";
import {useGetUserQuery} from "../../backend/apiSlice";
import {Loading} from "../Loading";
import {useSelector} from "react-redux";
import {AppState} from "../../storeDefinition";

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
  const turn = useSelector((state: AppState) => state.game.turn);
  const currentUser = useSelector((state: AppState) => state.client.currentUser);
  return <Button fullWidth variant="outlined" disabled={owner !== null || (owner === null && turn?.id !== currentUser?.id.id)} onClick={onClick}>
    {(isFetching || isLoading) && <Loading/>}
    {isError && <Typography>ERROR</Typography>}
    {isSuccess && owner !== null && user && <Typography>{user.user.alias}</Typography>}
    {owner === null && <Typography>Empty</Typography>}
  </Button>
}
