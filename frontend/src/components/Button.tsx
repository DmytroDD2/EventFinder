
import * as motion from "motion/react-client"
import { ReactNode,} from "react";
import { HTMLMotionProps } from "framer-motion";


type Props = HTMLMotionProps<'button'> & {
  children: ReactNode;
};


const Button = ({children, ...props}:Props)  => {
  return (
    <motion.button 
                   {...props}
                   whileTap={{ scale: 0.95 }}  
                   transition={{ duration: 0.2 }} 
                  >
                   {children}
    </motion.button>
  )
}

export default Button



