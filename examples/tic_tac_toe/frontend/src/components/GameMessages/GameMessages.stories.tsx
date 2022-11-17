import React from "react";
import {ComponentMeta, ComponentStory} from "@storybook/react";
import {GameMessages} from "./index";


export default {
    title: "TicTacToe/GameMessages",
    component: GameMessages
} as ComponentMeta<typeof GameMessages>;

const Template: ComponentStory<typeof GameMessages> = (args) => <GameMessages {...args} />;

export const NoMessages = Template.bind({});
NoMessages.args = {
    messages: []
};

export const SomeMessages = Template.bind({});
SomeMessages.args = {
    messages: ["first message", "another messages"]
};
