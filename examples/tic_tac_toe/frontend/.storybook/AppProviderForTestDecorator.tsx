// themeDecorator.js
import React from "react"
import {AppProviderForTest} from "../src/tools/test";
import {setupStore} from "../src/storeDefinition";
import {Story} from "@storybook/react";

const AppProviderForTestDecorator = (Story: Story, options: { args: any; parameters: any; }) => {
  const {parameters} = options;
  const {preloadedState = {}} = parameters;
  return <AppProviderForTest store={setupStore(preloadedState)}><Story/></AppProviderForTest>
}

export default AppProviderForTestDecorator
