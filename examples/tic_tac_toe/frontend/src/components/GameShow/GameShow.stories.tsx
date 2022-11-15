import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {GameShow} from "./index";
import {createGameId} from "../../tools/id";
import {plato, socrates} from "../../backend/fixtures/users";


export default {
  title: 'TicTacToe/GameShow',
  component: GameShow
} as ComponentMeta<typeof GameShow>;

const Template: ComponentStory<typeof GameShow> = (args) => <GameShow {...args} />;
const firstPlayer = socrates.id
const secondPlayer = plato.id

export const InProgress = Template.bind({});
InProgress.args = {
  gameState: {
    boardState: [[null, firstPlayer, null], [secondPlayer, null, null], [null, null, firstPlayer]],
    messages: [],
    stage: "IN_PROGRESS",
    turn: secondPlayer,
    gameId: createGameId(),
    winner: null
  },
  onPlace: () => null
};
