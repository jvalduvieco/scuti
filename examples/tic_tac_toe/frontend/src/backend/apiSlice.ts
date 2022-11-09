import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import {Id, ScoreListItem, User} from "../types";
import {createOperationId} from "../tools/id";
import {BACKEND_URL} from "../config";

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({baseUrl: process.env.NODE_ENV === "test" ? "" : BACKEND_URL}),
  tagTypes: ["TopThreeList"],
  endpoints: builder => ({
    createUser: builder.mutation<void, User>({
      query: (user: User) => ({
        url: '/commands',
        method: 'POST',
        body: {
          command: {
            type: 'CreateUser',
            payload: {
              ...user,
              operationId: createOperationId()
            }
          }
        },
      })
    }),
    getTopThreePlayers: builder.query<{ list: ScoreListItem[], parentOperationId: Id }, void>({
      query: operationId => ({
        url: '/queries',
        method: 'POST',
        body: {query: {type: 'GetTopThreePlayers', payload: {operationId: createOperationId()}}},
      }),
      providesTags: ["TopThreeList"]
    })
  })
})

export const {useCreateUserMutation, useGetTopThreePlayersQuery} = apiSlice
