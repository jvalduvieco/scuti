import {FC, ReactElement} from "react";
import {Typography} from "@mui/material";

type QueryHookStatus = { isFetching: boolean, isLoading: boolean, isError: boolean, isSuccess: boolean, error?: any }
type RenderOnSuccessProps = { queryStatus: QueryHookStatus | QueryHookStatus[], mustBeDefined: any | any[], children: ReactElement };
export const RenderOnSuccess: FC<RenderOnSuccessProps> = ({
                                                            queryStatus,
                                                            mustBeDefined,
                                                            children
                                                          }): ReactElement => {
  if (!Array.isArray(queryStatus)) {
    queryStatus = [queryStatus];
  }
  if (!Array.isArray(mustBeDefined)) {
    mustBeDefined = [mustBeDefined];
  }

  const isLoading = queryStatus.some(s => s.isLoading)
  const isFetching = queryStatus.some(s => s.isFetching)
  const isSuccess = queryStatus.every(s => s.isSuccess)
  const isError = queryStatus.some(s => s.isError)
  const error = queryStatus.filter(s => s.isError).map(s => s.error.toString()).join(",")
  const allDefined = mustBeDefined.every((v:any) => v !== null && v !== undefined)
  if (isLoading || isFetching) {
    return <Typography>Loading...</Typography>
  } else if (isSuccess && allDefined) {
    return children;
  } else if (isError) {
    return <Typography>An error occurred : {error}</Typography>
  }
  console.log(queryStatus)
  return <></>
}
