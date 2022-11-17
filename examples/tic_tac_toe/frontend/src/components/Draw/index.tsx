import {FC} from "react";
import {Handler} from "../../types";
import {Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography} from "@mui/material";

interface DrawProperties {
    restartGame: Handler
    gotoLobby: Handler
}

export const Draw: FC<DrawProperties> = ({restartGame, gotoLobby}: DrawProperties) =>
    <Dialog
        maxWidth="lg"
        open={true}
        onClose={gotoLobby}
    >
        <DialogTitle align="center">Oohh! It"s a Draw!</DialogTitle>
        <DialogContent>
            <Box sx={{
                display: "flex",
                flexDirection: "column",
                m: "auto",
                width: "fit-content",
            }}
            >
                <Typography>No winner this time</Typography>
            </Box>
        </DialogContent>
        <DialogActions>
            <Button onClick={gotoLobby}>Go to lobby</Button>
            <Button onClick={restartGame}>Restart with same players</Button>
        </DialogActions>
    </Dialog>
