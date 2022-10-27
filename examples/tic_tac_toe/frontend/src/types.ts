export type Handler = () => void
export type CellState = Id | null
export type BoardState = CellState[][]
export type GameStage = "PLAYER_WON" | "DRAW" | "IN_PROGRESS"

export type ConnectionStatus = "Online" | "Offline";
export type Id = { id: string }

export interface GameState {
  boardState: BoardState | null
  turn: Id | null
  messages: string[]
  stage: GameStage | null
  winner: Id | null
  gameId: Id | null
  firstPlayer: Id | null
  secondPlayer: Id | null
}
