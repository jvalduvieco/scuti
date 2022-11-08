import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import {Id} from "../types";
import {createOperationId} from "../tools/id";

// Define our single API slice object
export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({baseUrl: 'http://localhost:8080/'}),
  tagTypes: ["TopThreeList"],
  endpoints: builder => ({
    createUser: builder.mutation({
      query: userId => ({
        url: '/commands',
        method: 'POST',
        body: {command: {type: 'CreateUser', payload: {id: userId, alias: "an alias", createdAt: new Date().toISOString(), operationId: createOperationId()}}},
      })
    }),
    getTopThreePlayers: builder.query({
      query: operationId => ({
        url: '/queries',
        method: 'POST',
        body: {query: {type: 'GetTopThreePlayers', payload: {operationId}}},
      }),
      transformResponse: (responseData: { list: string[], parentOperationId: Id }) => {
        console.log("response", responseData)
        return responseData.list
      },
      providesTags: ["TopThreeList"]
    })
  })
})

export const {useCreateUserMutation, useGetTopThreePlayersQuery} = apiSlice
