import {CQRSClient} from "../tools/CQRSClient";
import {Id} from "../types";

class TicTacToeBackendClient extends CQRSClient {
  static async createGame(gameId: Id, creator: Id, operationId: Id) {
    return await TicTacToeBackendClient.doCommand("CreateGame",
        {
          operationId,
          gameId,
          creator,
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
