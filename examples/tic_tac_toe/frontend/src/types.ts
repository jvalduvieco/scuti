export type Handler = () => void
export type CellState = Id | null
export type BoardState = CellState[][]
export type GameStage = "PLAYER_WON" | "DRAW" | "IN_PROGRESS" | "WAITING_FOR_PLAYERS"

export type ConnectionStatus = "Online" | "Offline";
export type Id = { id: string }

export interface GameState {
  boardState: BoardState | null
  turn: Id | null
  messages: string[]
  stage: GameStage | null
  winner: Id | null
  gameId: Id | null
}

export interface GameClientState {
  currentUserId: Id | null
  opponentId: Id | null
}

export type ScoreListItem = { id: Id, score: number };

export function withPayloadType<T>() {
  return (t: T) => ({payload: t})
}

export type User = { id: Id, alias: string, createdAt: string };
