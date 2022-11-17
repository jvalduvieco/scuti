import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {GameAborted} from "./index";
import {action} from "@storybook/addon-actions";


export default {
    title: 'TicTacToe/GameAborted',
    component: GameAborted
} as ComponentMeta<typeof GameAborted>;

const Template: ComponentStory<typeof GameAborted> = (args) => <GameAborted {...args} />;

export const Show = Template.bind({});
Show.args = {
    gotoLobby: action("goToLobby"),
    restartGame: action("restartGame")
};
