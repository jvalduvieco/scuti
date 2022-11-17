import React from "react";
import {ComponentMeta, ComponentStory} from "@storybook/react";
import {Draw,} from "./index";
import {action} from "@storybook/addon-actions";


export default {
    title: "TicTacToe/Draw",
    component: Draw
} as ComponentMeta<typeof Draw>;

const Template: ComponentStory<typeof Draw> = (args) => <Draw {...args} />;

export const Show = Template.bind({});
Show.args = {
    gotoLobby: action("goToLobby"),
    restartGame: action("restartGame")
};
