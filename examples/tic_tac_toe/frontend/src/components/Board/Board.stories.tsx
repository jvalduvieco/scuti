import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {Board} from "./index";
import {createPlayerId} from "../../tools/id";

export default {
  title: 'TicTacToe/Board',
  component: Board
} as ComponentMeta<typeof Board>;
const firstPlayer = createPlayerId();
const secondPlayer = createPlayerId();
const Template: ComponentStory<typeof Board> = (args) => <Board {...args} />;

export const EmptyBoard = Template.bind({});
EmptyBoard.args = {
  state: [[null, null, null], [null, null, null], [null, null, null]],
  onPlace: () => null
};

export const SomePlaced = Template.bind({});
SomePlaced.args = {
  state: [[null, firstPlayer, null], [secondPlayer, null, null], [null, null, firstPlayer]],
  onPlace: () => null
};
