import {FC} from "react";
import {Handler, Id} from "../../types";
import {Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography} from "@mui/material";
import {useGetUserQuery} from "../../backend/apiSlice";

interface CongratulationsProps {
  winner: Id
  restartGame: Handler
  gotoLobby: Handler
}

export const CongratulationsPlayerWon: FC<CongratulationsProps> = ({
                                                                     winner,
                                                                     restartGame,
                                                                     gotoLobby
                                                                   }: CongratulationsProps) => {
  const {
    data: user,
      ...restGetUser
  } = useGetUserQuery(winner as Id, {skip: winner == null});
  return <Dialog
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
        <Typography>The winner is {user?.alias} !!</Typography>
      </Box>
    </DialogContent>
    <DialogActions>
      <Button onClick={gotoLobby}>Go to lobby</Button>
      <Button onClick={restartGame}>Restart with same players</Button>
    </DialogActions>
  </Dialog>
}
