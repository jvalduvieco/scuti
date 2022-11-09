import { rest } from 'msw'

export const handlers = [
  rest.post('/commands', (req, res, ctx) => {
    return res(
        ctx.status(200),
    )}),
  rest.post('/queries', (req, res, ctx) => {
    return res(
        ctx.status(200),
    )}),
  rest.post('/events', (req, res, ctx) => {
    return res(
        ctx.status(200),
    )})
]
