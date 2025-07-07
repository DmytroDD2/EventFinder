
import { useActionState} from 'react';
import styles from './index.module.css'
import { useAuthStore } from '@/store/authStore';
import { useLocation, useNavigate } from 'react-router-dom';
import { useThemeStore } from '@/store/themeStore';
import clsx from 'clsx';
import InputToggle from '@/components/InputToggle';
import * as motion from "motion/react-client"


const LoginPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuthStore();

    
    const {theme} = useThemeStore();
    
    const check_dark = theme === 'dark'
    
    const from = location.state?.from?.pathname || '/';
  
    const [error, submitAction, isPending] = useActionState(
      async (_: null | string, formData: FormData) => {
        try {
          const username = formData.get('username') as string;
          const password = formData.get('password') as string;
          
          await login(username, password);
          navigate(from, { replace: true });
          
          return null;
        } catch (err) {
          return err instanceof Error ? err.message : 'Login failed';
        }
      },
      null
    );
    const forgatePassword = () => {
      navigate('/password-reset');
    }
    return (
      <div className={clsx( styles.container, {[styles.dark_container]: check_dark})}>
        <h1>EventSphere</h1>
        <h2>Welcome back</h2>
        <p>Please log in to continue</p>
        {error && <div className="error-message">{error}</div>}
        
        <form action={submitAction} className={styles.form}>
          
          <fieldset className={clsx(styles.fieldset, check_dark && styles.dark_fieldset)}>
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username" 
              placeholder="Enter your username"
              required
              disabled={isPending}
            />
          </fieldset>
          
          <fieldset className={clsx(styles.fieldset, check_dark && styles.dark_fieldset)}
            style={{position: 'relative', paddingBottom: '0.4rem'}}>
            <InputToggle
             typeInput='password'
             name="password"
             placeholder='Enter your password'
             isPending={isPending}
             />
             <p className={styles.forgot_password}
                onClick={forgatePassword} 
             >Forgot password?</p>
          </fieldset>
          
          <motion.button 
            type="submit"
            disabled={isPending}
            className={isPending ? 'loading' : ''}
            // whileHover={{ scale: 1.05 }} 
            whileTap={{ scale: 0.95 }}   
            transition={{ duration: 0.2 }} 
          >
            {isPending ? 'Entering...' : 'Sing in'}
          </motion.button>
        </form>
      </div>
    );
  };
  

export default LoginPage