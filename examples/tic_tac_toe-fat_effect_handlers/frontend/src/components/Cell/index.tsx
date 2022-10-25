import {FC} from "react";
import {Button, Typography} from "@mui/material";
import {CellState, Handler} from "../../types";

interface CellProps {
  owner: CellState
  onClick: Handler
}
export const Cell: FC<CellProps> = ({owner, onClick}: CellProps) =>
    <Button fullWidth variant="outlined" disabled={owner !== null} onClick={onClick}>
      {owner !== null &&
          <Typography>{owner.id}</Typography>
      }
      {owner === null &&
          <Typography>Empty</Typography>
      }
    </Button>
