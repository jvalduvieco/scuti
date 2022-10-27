import React, {FC} from 'react';
import './App.css';
import {Provider} from 'react-redux';
import {appHistory, store} from "./store";
import {TicTacToeRoutes} from "./TicTacToeRoutes";
import {HistoryRouter} from "redux-first-history/rr6";
import {CssBaseline} from '@mui/material';

const App: FC = () =>
    <Provider store={store}>
      <HistoryRouter history={appHistory}>
        <CssBaseline/>
        <TicTacToeRoutes/>
      </HistoryRouter>
    </Provider>

export default App;
