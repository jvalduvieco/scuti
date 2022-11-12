import {FormProvider, SubmitHandler, useForm} from "react-hook-form";
import {User} from "../../types";
import {createUserId} from "../../tools/id";
import {useCreateUserMutation} from "../../backend/apiSlice";
import {Button, Grid, Paper, Typography} from "@mui/material";
import {yupResolver} from "@hookform/resolvers/yup";
import * as yup from "yup";
import {FormTextInput} from "../Form/FormTextInput";
import {UserAvatar} from "../UserAvatar";
import {userConnected} from "../../actions";
import {useDispatch} from "react-redux";

function completeUser(user: Partial<User>): User {
  return {...user, createdAt: new Date().toISOString(), id: createUserId()} as User
}

export default function UserForm() {
  const schema = yup.object({
    alias: yup.string().required()
  }).required();
  const methods = useForm<Partial<User>>({
    resolver: yupResolver(schema)
  });
  const [createUser] = useCreateUserMutation();
  const dispatch = useDispatch();

  const onSubmit: SubmitHandler<Partial<User>> = async user => {
    const newUser = completeUser(user);
    await createUser(newUser);
    dispatch(userConnected(newUser))
  };
  let alias = methods.watch("alias")

  return <Paper sx={{padding: 2, minHeight: "300px", width: "100%"}}>
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        <Grid container direction="column" spacing={1}>
          <Grid item xs justifyContent="center" display="flex">
            <Typography variant="h4">
              Create a user
            </Typography>
          </Grid>
          <Grid item xs={12} justifyContent="center" display="flex">
            <UserAvatar alias={alias ? alias : "?"}/>
          </Grid>
          <Grid item xs>
            <FormTextInput name="alias" fullWidth label={"Alias"}/>
          </Grid>

          <Grid item container direction="row" spacing={1} justifyContent="space-between">
            <Grid item>
              <Button onClick={methods.handleSubmit(onSubmit)} variant="contained">Create</Button>
            </Grid>
            <Grid item>
              <Button onClick={() => methods.reset()} variant={"outlined"}>Reset</Button>
            </Grid>
          </Grid>
        </Grid>
      </form>
    </FormProvider>
  </Paper>
}
