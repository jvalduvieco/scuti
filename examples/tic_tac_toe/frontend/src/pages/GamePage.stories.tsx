import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {GamePage} from './GamePage';
import {plato, socrates} from "../backend/fixtures/users";


export default {
  title: 'TicTacToe/GamePage',
  component: GamePage
} as ComponentMeta<typeof GamePage>;

const Template: ComponentStory<typeof GamePage> = (args) => <GamePage {...args} />;

export const WaitingForPlayers = Template.bind({});
WaitingForPlayers.parameters = {
  preloadedState: {
    client: {
      currentUserId: socrates.id,
      opponentId: plato.id
    },
    game: {
      stage: "WAITING_FOR_PLAYERS"
    }
  },
};

export const PlayerWon = Template.bind({});
PlayerWon.parameters = {
  preloadedState: {
    client: {
      currentUserId: socrates.id,
      opponentId: plato.id
    },
    game: {
      stage: "PLAYER_WON",
      winner: socrates.id
    }
  },
};

export const DrawStage = Template.bind({});
DrawStage.parameters = {
  preloadedState: {
    client: {
      currentUserId: socrates.id,
      opponentId: plato.id
    },
    game: {
      stage: "DRAW"
    }
  },
};


export const InProgress = Template.bind({});
InProgress.parameters = {
  preloadedState: {
    client: {
      currentUserId: socrates.id,
      opponentId: plato.id
    },
    game: {
      stage: "IN_PROGRESS",
      turn: socrates.id,
      boardState: [[null, socrates.id, null], [plato.id, null, null], [null, null, socrates.id]],
      messages: ["Nice game in progress"]
    }
  },
};
