import {FC} from "react";
import {Grid, Paper, styled, Typography} from "@mui/material";
import {GameStage, Id} from "../../types";

interface GameStageProps {
  stage: GameStage
  winner: Id | null
  turn: Id | null
}

const Item = styled(Paper)(() => ({
  textAlign: 'center',
}));

export const ShowGameStage: FC<GameStageProps> = ({stage, winner, turn}: GameStageProps) =>
    <Grid container direction="column" spacing={1}>
      <Grid item>
        <Item>
          <Typography variant="h3">
            {stage}
          </Typography>
        </Item>
      </Grid>
      {stage === "PLAYER_WON" && winner !== null && <Grid item>
          <Item>
              <Typography>
                {winner.id}
              </Typography>
          </Item>
      </Grid>}
      {stage === "DRAW" && <Grid item>
          <Item>
              <Typography>
                  No winner this time
              </Typography>
          </Item>
      </Grid>}
      {stage === "IN_PROGRESS" && turn && <Grid item>
          <Item>
              <Typography>
                  It's {turn.id} turn
              </Typography>
          </Item>
      </Grid>}
    </Grid>;
