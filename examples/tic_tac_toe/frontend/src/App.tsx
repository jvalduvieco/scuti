import React, {FC} from "react";
import "./App.css";
import {Provider} from "react-redux";
import {TicTacToeRoutes} from "./TicTacToeRoutes";
import {CssBaseline} from "@mui/material";
import {store} from "./store";
import {ReduxRouter} from "@lagunovsky/redux-react-router";
import {appHistory} from "./storeDefinition";

const App: FC = () =>
    <Provider store={store}>
        <ReduxRouter history={appHistory}>
            <CssBaseline/>
            <TicTacToeRoutes/>
        </ReduxRouter>
    </Provider>

export default App;
