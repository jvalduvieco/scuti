import {Button, Container, Grid, Typography} from "@mui/material";
import {FC} from "react";

interface LobbyProps {
  onNewGame: () => void
}

export const Lobby: FC<LobbyProps> = ({onNewGame}) =>
    <Container maxWidth="sm">
      <Grid container direction="column" alignContent="center" justifyContent="center" sx={{height: "100vh"}} spacing={3}>
        <Grid item>
          <Typography variant="h3">
            Welcome to tic tac toe!
          </Typography>
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={onNewGame} fullWidth>Play!</Button>
        </Grid>
      </Grid>
    </Container>
