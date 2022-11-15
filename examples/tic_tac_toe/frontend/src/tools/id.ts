import {v4 as uuidv4} from "uuid";
import {Id} from "../types";

export const createOperationId: () => Id = () => ({id: uuidv4()})
export const createGameId: () => Id = () => ({id: uuidv4()})
export const createPlayerId: () => Id = () => ({id: uuidv4()})
export const createUserId: () => Id = () => ({id: uuidv4()})
