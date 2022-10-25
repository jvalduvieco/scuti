import {FC} from "react";
import {Grid} from "@mui/material";
import {Board} from "../Board";
import {GameMessages} from "../GameMessages";
import {ShowGameStage} from "../ShowGameStage";
import {GameState} from "../../types";

interface GameShowProps {
  gameState: GameState
  onPlace: (x: number, y: number) => void
}

export const GameShow: FC<GameShowProps> = ({
                                              gameState: {boardState, messages, stage, winner, turn},
                                              onPlace
                                            }: GameShowProps) =>
    <Grid container direction="column" spacing={2} justifyContent="space-between" sx={{height: "100%", padding: "16px"}}>
      <Grid item>
        <ShowGameStage stage={stage!} winner={winner} turn={turn}/>
      </Grid>
      <Grid item>
        <Board state={boardState!} onPlace={onPlace}/>
      </Grid>
      <Grid item>
        <GameMessages messages={messages}/>
      </Grid>

    </Grid>
