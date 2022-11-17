import {setupServer} from 'msw/node'
import {mswTestHandlers} from './handlers'

export const server = setupServer(...mswTestHandlers)
