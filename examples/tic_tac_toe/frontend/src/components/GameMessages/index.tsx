import {FC} from "react";
import {Grid, Paper, Typography} from "@mui/material";

interface GameMessagesProps {
  messages: string[]
}

export const GameMessages: FC<GameMessagesProps> = ({messages}: GameMessagesProps) =>
    <Paper sx={{padding: "8px", height: "20vh"}}>
      <Grid container direction="column" spacing={1}>
        {messages.map((message, index) =>
            <Grid item key={index}>
              <Typography>
                {message}
              </Typography>
            </Grid>
        )}
      </Grid>
    </Paper>
