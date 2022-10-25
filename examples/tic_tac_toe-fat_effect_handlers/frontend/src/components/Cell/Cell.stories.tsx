import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {Cell} from "./index";
import {createPlayerId} from "../../tools/id";

export default {
  title: 'TicTacToe/Cell',
  component: Cell
} as ComponentMeta<typeof Cell>;

const Template: ComponentStory<typeof Cell> = (args) => <Cell {...args} />;

export const EmptyCell = Template.bind({});
EmptyCell.args = {
  owner: null,
  onClick: () => null
};

export const APlayer = Template.bind({});
APlayer.args = {owner: createPlayerId(), onClick: () => null};
