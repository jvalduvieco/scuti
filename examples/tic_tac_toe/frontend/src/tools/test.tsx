import React, {FC, PropsWithChildren, ReactNode} from 'react'
import type {RenderOptions} from '@testing-library/react'
import {render} from '@testing-library/react'
import type {PreloadedState} from '@reduxjs/toolkit'
import {Provider} from 'react-redux';
import {AppState, AppStore, setupStore} from "../storeDefinition";
import {MemoryRouter} from 'react-router';


// This type interface extends the default options for render from RTL, as well
// as allows the user to specify other things such as initialState, store.
interface ExtendedRenderOptions extends Omit<RenderOptions, 'queries'> {
    preloadedState?: PreloadedState<AppState>
    store?: AppStore
}

type Props = {
    store: AppStore
    children: ReactNode
}
export const AppProviderForTest: FC<Props> = ({store, children}) =>
    <Provider store={store}>
        <MemoryRouter>
            {children}
        </MemoryRouter>
    </Provider>

export function renderWithProviders(
    ui: React.ReactElement,
    {
        preloadedState = {},
        // Automatically create a store instance if no store was passed in
        store = setupStore(preloadedState),
        ...renderOptions
    }: ExtendedRenderOptions = {}
) {
    function Wrapper({children}: PropsWithChildren<{}>) {
        return <AppProviderForTest store={store}> {children} </AppProviderForTest>
    }

    return {store, ...render(ui, {wrapper: Wrapper, ...renderOptions})}
}
