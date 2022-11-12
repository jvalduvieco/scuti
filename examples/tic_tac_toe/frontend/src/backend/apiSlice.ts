import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react"
import {Id, ScoreListItem, User} from "../types";
import {createOperationId} from "../tools/id";
import {BACKEND_URL} from "../config";

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({baseUrl: process.env.NODE_ENV === "test" ? "" : BACKEND_URL}),
  tagTypes: ["TopThreeList", "UsersOnline", "User"],
  endpoints: builder => ({
    createUser: builder.mutation<void, User>({
      query: (user: User) => ({
        url: "/commands",
        method: "POST",
        body: {
          command: {
            type: "CreateUser",
            payload: {
              ...user,
              operationId: createOperationId()
            }
          }
        },
      })
    }),
    userConnected: builder.mutation<void, Id>({
      query: (id: Id) => ({
        url: "/events",
        method: "POST",
        body: {
          event: {
            type: "UserConnected",
            payload: {
              id,
              operationId: createOperationId()
            }
          }
        },
      }),
      invalidatesTags: ["UsersOnline"]
    }),
    userInvited: builder.mutation<void, { host: Id, invited: Id, game: Id }>({
      query: ({host, invited, game}) => ({
        url: "/events",
        method: "POST",
        body: {
          event: {
            type: "UserInvited",
            payload: {
              host,
              invited,
              game,
              operationId: createOperationId()
            }
          }
        },
      }),
      invalidatesTags: ["UsersOnline"]
    }),
    joinGame: builder.mutation<void, { player: Id, game: Id }>({
      query: ({player, game}) => ({
        url: "/commands",
        method: "POST",
        body: {
          command: {
            type: "JoinGame",
            payload: {
              playerId: player,
              gameId: game,
              operationId: createOperationId()
            }
          }
        },
      }),
      invalidatesTags: ["UsersOnline"]
    }),
    getTopThreePlayers: builder.query<{ list: ScoreListItem[], parentOperationId: Id }, void>({
      query: () => ({
        url: "/queries",
        method: "POST",
        body: {query: {type: "GetTopThreePlayers", payload: {operationId: createOperationId()}}},
      }),
      providesTags: ["TopThreeList"]
    }),
    getUsersOnline: builder.query<{ onlineUsers: Id[], parentOperationId: Id }, void>({
      query: () => ({
        url: "/queries",
        method: "POST",
        body: {query: {type: "GetUsersOnline", payload: {operationId: createOperationId()}}},
      }),
      providesTags: ["UsersOnline"]
    }),
    getUser: builder.query<{ user: User, parentOperationId: Id }, Id>({
      query: (userId: Id) => ({
        url: "/queries",
        method: "POST",
        body: {query: {type: "GetUser", payload: {operationId: createOperationId(), id: userId}}},
      }),
      providesTags: (result: { user: User, parentOperationId: Id } | undefined, error, arg) => result ? [
        "User",
        {type: "User", id: result.user.id.id}
      ] : []
    })
  })
})

export const {
  useCreateUserMutation,
  useUserInvitedMutation,
  useJoinGameMutation,
  useGetTopThreePlayersQuery,
  useGetUsersOnlineQuery,
  useGetUserQuery
} = apiSlice

export const userFetched = apiSlice.endpoints.getUser.matchFulfilled
export const userJoined = apiSlice.endpoints.joinGame.matchFulfilled
