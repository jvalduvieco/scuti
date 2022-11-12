import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {ShowTurn} from "./index";
import { createPlayerId } from '../../tools/id';


export default {
  title: 'TicTacToe/ShowTurn',
  component: ShowTurn
} as ComponentMeta<typeof ShowTurn>;

const Template: ComponentStory<typeof ShowTurn> = (args) => <ShowTurn {...args} />;

export const InProgress = Template.bind({});
InProgress.args = {
  turn: createPlayerId()
};
