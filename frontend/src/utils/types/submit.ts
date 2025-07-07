
// import { NavigateFunction } from 'react-router-dom';

type PasswordReset = {
    username: string;
    password: string;
    password_reset_question: string;
  };


type RegisterFieldNames = {
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    confirm_password: string;
    password_reset_question: string;
    role: string;
}

type PasswordChange = {
    password: string;
}

type changePassowrd = (data: FormData) => Promise<void>;



type FormInputData = PasswordReset | PasswordChange | RegisterFieldNames;



type OnSubmitParams = {
    data: FormInputData;
    changePassowrd: changePassowrd;
    navigate: () => void;
}

type TypeInput = "change" | "reset" | "registration" 



type RoleType = "admin" | "user" ;
export type { RoleType,TypeInput, PasswordReset, PasswordChange, changePassowrd, FormInputData, OnSubmitParams };