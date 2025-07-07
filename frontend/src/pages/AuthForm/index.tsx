
import Button from "@/components/Button";
import styles from "./index.module.css";
import Slider from 'react-range-slider-input';
import clsx from "clsx";
import InputToggle from "@/components/InputToggle";
import { useThemeStore } from "@/store/themeStore";
import MarkV from "@/assets/icons_svg/mark_v.svg?react";
import MarkX from "@/assets/icons_svg/mark_x.svg?react";
import { yupResolver } from '@hookform/resolvers/yup';
import { SubmitHandler, useForm } from "react-hook-form";
import {calculatePasswordStrength, createPasswordSchema, getPasswordRequirements} from "@/utils/validation";
import useChangePassword from "@/hooks/profile/useChangePassword";
import { useNavigate, useParams} from 'react-router-dom';
import { inputlistFunction, onSubmit } from "@/utils/submit";
import { FormInputData, TypeInput} from "@/utils/types/submit";



const AuthForm = ({actionType}: {actionType: TypeInput}) => {
 
  const navigate = useNavigate(); 
  const {theme} = useThemeStore();

  const check_dark = theme === 'dark'
  
  const {userId} = useParams()

  const passwordSchema = createPasswordSchema(actionType)

  const inputlist = inputlistFunction(actionType);

  const {changePassowrd} = useChangePassword(actionType, userId);


  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    } = useForm({ resolver: yupResolver(passwordSchema), mode: "onChange"})

    
  const newPassword = watch('password', '');

    
  const { strength, percentage }  = calculatePasswordStrength(newPassword);
  const requirements = getPasswordRequirements(newPassword);
  
  const redirctOnChange = () =>{
    navigate(
      userId 
        ?`/admin/${userId}` 
          :'/profile',
      { replace: true }
    )
  }
  const handleFormSubmit: SubmitHandler<FormInputData> = (data) => {
    onSubmit({
      data,
      changePassowrd: changePassowrd, 
      navigate: redirctOnChange,
      tipeToSubmit: actionType
    });
  };
    

  const onCancel: React.MouseEventHandler<HTMLButtonElement> = (e) => {
    e.preventDefault();
    navigate(-1);
  }

  return (
    <div className={clsx(styles.container, check_dark && styles.dark_container)}>
      <div className={styles.container_child}>

      <div className={clsx(styles.header, check_dark && styles.dark_header)}>
        {actionType === 'registration' ? 
        <>
           <h2 className={styles.regist_h}>Create Your Account</h2> 
           <p className={styles.regist_p}>Join our community today</p>
        </>
        :< >
           <h2>Change Password</h2> 
           <p>Pleas enter your password and new password below</p>
        </>}
      </div>

      <form 
        onSubmit={handleSubmit(handleFormSubmit)}
        className={styles.form_container}>

      {inputlist.map((input, index) => (
        <fieldset key={index} className={clsx(styles.fieldset, check_dark && styles.dark_fieldset)}>
          <InputToggle
            label={input.label}
            {...actionType === 'registration' && input.name === "email" && {type: "email"}}
            {...(["password", "confirm_password"].includes(input.name) && {typeInput: "password"})}
            placeholder={input.placeholder}
            {...register(input.name as keyof FormInputData)}
          />
          <p className={styles.error}>{errors[input.name as keyof FormInputData]?.message}</p>
        </fieldset>     
        ))}
      
      <ul className={styles.requirements}>
        <h3>Password Requirments</h3>
        
        {requirements.map((req, index) => (
        <li key={index} className={clsx(styles.invalid_req,{ [styles.valid_req]: req.isValid })}>
        {req.isValid ?
         <MarkV className={styles.v}/> :
         <MarkX className={styles.x}/>}
        {req.text}
        </li>
        ))}

      </ul>
      <div className={styles.slider_container} >

        <div className={styles.password_strength}>
          <p>Password Strength</p>
          <span>{strength}</span>
        </div>
        
        <Slider
          min={0}
          max={100}
          value={[0, percentage]}
          disabled
          id={clsx("range-slider-gradient")}
          className="margin-lg"
        />
        <div className={styles.button_container}>
          <Button onClick={onCancel}>Cancel</Button>
          <Button type="submit" >{actionType === 'registration' ? 'Register' : 'Save Changes'}</Button>
        </div>
        </div>
      </form>  
      </div>
    </div>
  )
}

export default AuthForm