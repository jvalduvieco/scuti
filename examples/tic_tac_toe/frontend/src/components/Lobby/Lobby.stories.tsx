import React from 'react';
import {ComponentMeta, ComponentStory} from '@storybook/react';
import {Lobby} from "./index";


export default {
    title: 'TicTacToe/Lobby',
    component: Lobby
} as ComponentMeta<typeof Lobby>;

const Template: ComponentStory<typeof Lobby> = (args) => <Lobby {...args} />;

export const Empty = Template.bind({});
Empty.args = {};
