import {FC} from "react";
import {Grid} from "@mui/material";
import {Cell} from "../Cell";
import {BoardState} from "../../types";

interface BoardProps {
    state: BoardState
    onPlace: (x: number, y: number) => void
}

export const Board: FC<BoardProps> = ({state, onPlace}: BoardProps) => {
    return <Grid container direction='column' spacing={1}>
        {
            state.map((row, y) =>
                <Grid item container direction='row' key={`b${y}`} spacing={1}>
                    {row.map((owner, x) =>
                        <Grid item xs={4} key={`c${x + y}`}>
                            <Cell owner={owner} onClick={() => onPlace(x, y)}/>
                        </Grid>
                    )}
                </Grid>
            )}
    </Grid>
}
