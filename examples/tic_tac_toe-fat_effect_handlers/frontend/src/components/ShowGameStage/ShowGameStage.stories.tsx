import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {ShowGameStage} from "./index";
import { createPlayerId } from '../../tools/id';


export default {
  title: 'TicTacToe/ShowGameStage',
  component: ShowGameStage
} as ComponentMeta<typeof ShowGameStage>;

const Template: ComponentStory<typeof ShowGameStage> = (args) => <ShowGameStage {...args} />;

export const InProgress = Template.bind({});
InProgress.args = {
  stage: "IN_PROGRESS",
  turn: createPlayerId()
};

export const Draw = Template.bind({});
Draw.args = {
  stage: "DRAW"
};
export const PlayerWon = Template.bind({});
PlayerWon.args = {
  stage: "PLAYER_WON",
  winner: createPlayerId()
};
