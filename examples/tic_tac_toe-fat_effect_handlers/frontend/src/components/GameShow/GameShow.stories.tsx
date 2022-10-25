import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {GameShow} from "./index";
import {createGameId, createPlayerId} from "../../tools/id";


export default {
  title: 'TicTacToe/GameShow',
  component: GameShow
} as ComponentMeta<typeof GameShow>;

const Template: ComponentStory<typeof GameShow> = (args) => <GameShow {...args} />;
const firstPlayer = createPlayerId()
const secondPlayer = createPlayerId()

export const InProgress = Template.bind({});
InProgress.args = {
  gameState: {
    boardState: [[null, firstPlayer, null], [secondPlayer, null, null], [null, null, firstPlayer]],
    messages: [],
    stage: "IN_PROGRESS",
    turn: secondPlayer,
    gameId: createGameId(),
    winner: null,
    firstPlayer,
    secondPlayer,
  },
  onPlace: () => null
};

export const Draw = Template.bind({});
Draw.args = {
  gameState: {
    boardState: [[null, firstPlayer, null], [secondPlayer, null, null], [null, null, firstPlayer]],
    messages: [],
    stage: "DRAW",
    turn: secondPlayer,
    gameId: createGameId(),
    winner: null,
    firstPlayer,
    secondPlayer,
  },
  onPlace: () => null
};
export const PlayerWon = Template.bind({});
PlayerWon.args = {
  gameState: {
    boardState: [[null, firstPlayer, null], [secondPlayer, null, null], [null, null, firstPlayer]],
    messages: ["Player 1 played 1, 0", "Player 2 played 0, 1", "Player 1 played 2, 2"],
    stage: "IN_PROGRESS",
    turn: secondPlayer,
    winner: firstPlayer,
    firstPlayer,
    secondPlayer,
    gameId: createGameId()
  },
  onPlace: () => null
};
