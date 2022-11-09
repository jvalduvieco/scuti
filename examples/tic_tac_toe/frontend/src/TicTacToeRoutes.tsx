import {Routes} from "react-router-dom";
import {Route} from "react-router";
import {FC} from "react";
import GamePage from "./pages/GamePage";
import {Lobby} from "./components/Lobby";

export enum AppRoutes {
  HOME = "/",
  GAME_SCREEN = "/game"
}


export const TicTacToeRoutes: FC = () => {
  return <Routes>
    <Route path={`${AppRoutes.HOME}`} element={<Lobby/>}/>
    <Route path={`${AppRoutes.GAME_SCREEN}/:gameId`} element={<GamePage/>}/>
  </Routes>
}
