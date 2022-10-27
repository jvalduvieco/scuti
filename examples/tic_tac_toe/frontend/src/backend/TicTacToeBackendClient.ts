import {CQRSClient} from "../tools/CQRSClient";
import {Id} from "../types";

class TicTacToeBackendClient extends CQRSClient {
  static async createNewGame(gameId: Id, player1: Id, player2: Id, operationId: Id) {
    return await TicTacToeBackendClient.doCommand("NewGame",
        {
          operationId: operationId,
          gameId: gameId,
          firstPlayer: player1,
          secondPlayer: player2
        });
  }

  static async placeMark(gameId: Id, player: Id, x: number, y: number, operationId: Id) {
    return await TicTacToeBackendClient.doCommand("PlaceMark",
        {
          operationId: operationId,
          gameId: gameId,
          player: player,
          x,
          y
        });
  }
}

export default TicTacToeBackendClient;
