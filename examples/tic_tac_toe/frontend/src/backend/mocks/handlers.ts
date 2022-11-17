import {rest} from "msw"
import {plato, socrates} from "../fixtures/users";

const users = {
    [socrates.id.id]: socrates,
    [plato.id.id]: plato
}

export const mswTestHandlers = [
    rest.post(/\/commands/, (req, res, ctx) => {
        return res(
            ctx.status(200),
        )
    }),
    rest.post(/\/queries/, async (req, res, ctx) => {
        const {query} = await req.json()
        switch (query.type) {
            case "GetUser": {
                const {operationId, id} = query.payload;
                return res(
                    ctx.json({
                        user: users[id.id],
                        parentOperationId: operationId
                    })
                )
            }
            case "GetUsersOnline": {
                const {operationId} = query.payload;
                return res(
                    ctx.json({
                        onlineUsers: Object.keys(users).map(e => ({id: e})),
                        parentOperationId: operationId
                    })
                )
            }
            case "GetTopThreePlayers": {
                const {operationId} = query.payload;
                return res(
                    ctx.json({
                        list: Object.keys(users).map((e, index) => ({id: {id: e}, score: 100 + index * 20})),
                        parentOperationId: operationId
                    })
                )
            }
            default:
                console.error("This mock can not handle given query: ", query)
                return res(
                    ctx.status(500)
                )
        }
    }),
    rest.post(/\/events/, (req, res, ctx) => {
        return res(
            ctx.status(200),
        )
    })
]
