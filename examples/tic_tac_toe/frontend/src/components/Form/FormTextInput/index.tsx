import {FC} from "react";
import {Controller, useFormContext} from "react-hook-form";
import {TextField, TextFieldProps} from "@mui/material";

type IFormTextInputProps = {
    name: string;
} & TextFieldProps;
export const FormTextInput: FC<IFormTextInputProps> = ({name, ...otherProps}) => {
    const {
        control,
        formState: {errors},
    } = useFormContext();

    return (
        <Controller control={control} name={name} defaultValue="" render={({field}) => (
            <TextField
                {...otherProps}
                {...field}
                error={!!errors[name]}
                helperText={errors[name] ? errors[name]!.message as string : ''}
            />
        )}
        />
    );
};
