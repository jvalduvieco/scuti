import React, {FC} from 'react';
import './App.css';
import {Provider} from 'react-redux';
import {store} from "./store";
import {TicTacToeRoutes} from "./TicTacToeRoutes";
import {CssBaseline} from '@mui/material';
import {HashRouter} from 'react-router-dom';

const App: FC = () =>
    <HashRouter>
      <Provider store={store}>
        <CssBaseline/>
        <TicTacToeRoutes/>
      </Provider>
    </HashRouter>

export default App;
