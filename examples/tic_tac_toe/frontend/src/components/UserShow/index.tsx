import {Grid, Paper, Typography} from "@mui/material";
import {UserAvatar} from "../UserAvatar";
import {FC} from "react";

export const UserShow: FC<{ alias: string }> = ({alias}) => {

    return <Paper sx={{padding: 2, minHeight: "300px"}}>
        <Grid container direction="column" spacing={1}>
            <Grid item xs={12} justifyContent="center" display="flex">
                <UserAvatar alias={alias}/>
            </Grid>
            <Grid item xs justifyContent="center" display="flex">
                <Typography variant="h5">{alias}</Typography>
            </Grid>
        </Grid>
    </Paper>
}
