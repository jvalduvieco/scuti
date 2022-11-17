import React from "react";
import {ComponentMeta, ComponentStory} from "@storybook/react";
import {ShowTurn} from "./index";
import {plato} from "../../backend/fixtures/users";


export default {
    title: "TicTacToe/ShowTurn",
    component: ShowTurn
} as ComponentMeta<typeof ShowTurn>;

const Template: ComponentStory<typeof ShowTurn> = (args) => <ShowTurn {...args} />;

export const InProgress = Template.bind({});
InProgress.args = {
    turn: plato.id
};
