import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {CongratulationsPlayerWon,} from "./index";
import {action} from "@storybook/addon-actions";
import {plato} from '../../backend/fixtures/users';


export default {
    title: 'TicTacToe/CongratulationsPlayerWon',
    component: CongratulationsPlayerWon
} as ComponentMeta<typeof CongratulationsPlayerWon>;

const Template: ComponentStory<typeof CongratulationsPlayerWon> = (args) => <CongratulationsPlayerWon {...args} />;

export const Show = Template.bind({});
Show.args = {
    winner: plato.id,
    gotoLobby: action("goToLobby"),
    restartGame: action("restartGame")
};
