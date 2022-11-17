import {FC} from "react";
import {Handler} from "../../types";
import {Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography} from "@mui/material";

interface GameAbortedProps {
    restartGame: Handler
    gotoLobby: Handler
}

export const GameAborted: FC<GameAbortedProps> = ({
                                                      restartGame,
                                                      gotoLobby
                                                  }: GameAbortedProps) => {
    return <Dialog
        maxWidth="lg"
        open={true}
        onClose={gotoLobby}
    >
        <DialogTitle align="center">Doh! Game was aborted!</DialogTitle>
        <DialogContent>
            <Box sx={{
                display: 'flex',
                flexDirection: 'column',
                m: 'auto',
                width: 'fit-content',
            }}
            >
                <Typography>The game was aborted due a user timeout</Typography>
            </Box>
        </DialogContent>
        <DialogActions>
            <Button onClick={gotoLobby}>Go to lobby</Button>
            <Button onClick={restartGame}>Restart with same players</Button>
        </DialogActions>
    </Dialog>
}
