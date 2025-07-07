
import { SubmitHandler} from "react-hook-form";
import { OnSubmitParams, TypeInput } from "./types/submit";


const onSubmit: SubmitHandler<OnSubmitParams& { tipeToSubmit: TypeInput }> = async (
    {
     data,
     changePassowrd,
     navigate,
     tipeToSubmit,
    }: OnSubmitParams& { tipeToSubmit: TypeInput }

) => {
    const queryParams = new FormData();
    if ("email" in data) {
        queryParams.append('email', data.email);
        queryParams.append('first_name', data.first_name);
        queryParams.append('last_name', data.last_name);
        queryParams.append('role', data.role);
        queryParams.append('username', data.username);
        queryParams.append('password_reset_question', data.password_reset_question);
    }
    else if ("username" in data ) {
        queryParams.append('username', data.username);
        queryParams.append('password_reset_question', data.password_reset_question);
        queryParams.append('new_password', data.password);
    }
    if ("password" in data) {
        queryParams.append('password', data.password);
    }

    try {
        await changePassowrd(queryParams);
        alert(tipeToSubmit === "registration" ? "Registration successful!" : "Password changed successfully!");
    
        navigate();
    } catch (error) {
        // alert("Failed to change password. Please try again.");
        alert(tipeToSubmit === "registration" ? "Registration failed. Please try again." : "Password change failed. Please try again.");
        // console.error("Error changing password:", error);
        console.error(tipeToSubmit === "registration" ? "Error during registration:" : "Error during password change:", error);
    }
    
};



type RegisterFieldNames = { 
    name:
      "password" 
    | "confirm_password" 
    | "username" 
    | "last_name" 
    | "first_name" 
    | "email" 
    | "password_reset_question" 
    | "role";
    label: string;
    placeholder: string;
}[]



type  inputPassword ={
     name: "password" | "confirm_password";
     label: string; 
     placeholder: string 
     }[]


type inputliresetPassword = {
     name: "username" | "password_reset_question" | "password" | "confirm_password";
     label: string;
     placeholder: string 
     }[]


const inputlistFunction = (type: TypeInput): inputPassword | inputliresetPassword | RegisterFieldNames => {
    if(type === "registration") {
        return [
            { name: "role", label: "Role", placeholder: "user or admin"},
            { name: "first_name", label: "First Name", placeholder: "Enter your first name"},
            { name: "last_name", label: "Last Name", placeholder: "Enter your last name"},
            { name: "email", label: "Email", placeholder: "Enter your email"},
            { name: "username", label: "Username", placeholder: "Enter your username"},
            { name: "password_reset_question", label: "Password Reset Question", placeholder: "Enter your password reset question"},
            { name: "password", label: "Password", placeholder: "Enter your new password"},
            { name: "confirm_password", label: "Confirm Password", placeholder: "Confirm your password"}
    ]}
    if (type === "change") {
        return [
            { name: "password", label: "New Password", placeholder: "Enter your new password"},
            { name: "confirm_password", label: "Confirm Password", placeholder: "Confirm your password"}
        ]
    } else {
        return [
            { name: "username", label: "Username", placeholder: "Enter your username"},
            { name: "password_reset_question", label: "Password Reset Question", placeholder: "Enter your password reset question"},
            { name: "password", label: "New Password", placeholder: "Enter your new password"},
            { name: "confirm_password", label: "Confirm Password", placeholder: "Confirm your password"}
        ]
    }
}
  


export {onSubmit, inputlistFunction}