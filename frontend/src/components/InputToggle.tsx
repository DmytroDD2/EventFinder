
import clsx from 'clsx';
import { useState } from 'react'
import { AiFillEyeInvisible, AiFillEye } from "react-icons/ai";

type InputToggleProps = {
  isPending?: boolean
  name: string
  placeholder?: string
  className?: string
  label?: string,
  typeInput?: "text" | "password"
  
}

const InputToggle = ({
   isPending,
   name,
   placeholder,
   className,
   label,
   typeInput,
  ...props
  }: InputToggleProps & React.InputHTMLAttributes<HTMLInputElement>) => {
  const [showPassword, setShowPassword] = useState(false);
  return (
  <>
    <label htmlFor={name}>{label || "Password"}</label>
    <div className={clsx('input-password', className)}>
      <input 
        type={showPassword ? "text" : typeInput}
        id={name}
        name={name}
        placeholder={placeholder ||"Enter your password"}
        required
        disabled={isPending}
        {...props}
      />
      {typeInput === "password" && (
        showPassword ? (
          <AiFillEye
            className='eye-icon'
            onClick={() => setShowPassword((prevState) => !prevState)}
          />
        ) : (
          <AiFillEyeInvisible
            className='eye-icon'
            onClick={() => setShowPassword((prevState) => !prevState)}
          />
        )
      )}
    </div>
  </>
  )
}

export default InputToggle