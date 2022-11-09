import React, {FC} from 'react';
import './App.css';
import {Provider} from 'react-redux';
import {TicTacToeRoutes} from "./TicTacToeRoutes";
import {CssBaseline} from '@mui/material';
import {HashRouter} from 'react-router-dom';
import {store} from "./store";

const App: FC = () =>
    <HashRouter>
      <Provider store={store}>
        <CssBaseline/>
        <TicTacToeRoutes/>
      </Provider>
    </HashRouter>

export default App;
