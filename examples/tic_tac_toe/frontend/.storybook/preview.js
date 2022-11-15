import AppProviderForTestDecorator from "./AppProviderForTestDecorator";
import {initialize, mswDecorator} from 'msw-storybook-addon';
import {mswTestHandlers} from "../src/backend/mocks/handlers";
import {socrates} from "../src/backend/fixtures/users";

initialize();

export const parameters = {
    actions: {argTypesRegex: "^on[A-Z].*"},
    controls: {
        matchers: {
            color: /(background|color)$/i,
            date: /Date$/,
        },
    },
    preloadedState: {client: {currentUserId: socrates.id}},
    msw: {
        handlers: mswTestHandlers
    },
}
export const decorators = [mswDecorator, AppProviderForTestDecorator]
