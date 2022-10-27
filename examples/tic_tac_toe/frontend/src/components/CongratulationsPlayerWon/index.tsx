import {FC} from "react";
import {Handler, Id} from "../../types";
import {Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography} from "@mui/material";

interface CongratulationsProps {
  winner: Id
  restartGame: Handler
  gotoLobby: Handler
}

export const CongratulationsPlayerWon: FC<CongratulationsProps> = ({
                                                                     winner,
                                                                     restartGame,
                                                                     gotoLobby
                                                                   }: CongratulationsProps) =>
    <Dialog
        maxWidth="lg"
        open={true}
        onClose={gotoLobby}
    >
      <DialogTitle align="center">Congratulations!</DialogTitle>
      <DialogContent>
        <Box sx={{
          display: 'flex',
          flexDirection: 'column',
          m: 'auto',
          width: 'fit-content',
        }}
        >
          <Typography>The winner is {winner.id} !!</Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={gotoLobby}>Go to lobby</Button>
        <Button onClick={restartGame}>Restart with same players</Button>
      </DialogActions>
    </Dialog>
