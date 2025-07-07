import { useThemeStore } from '../store/themeStore';
import Light from '@/assets/icons/light.png';
import Dark from '@/assets/icons/dark.png';
import * as motion from "motion/react-client"

const ThemeToggle = () => {
  const { theme, toggleTheme } = useThemeStore();

  return (
    
    <motion.div onClick={toggleTheme} style={{
        display: 'flex',    
        cursor: 'pointer',
        width: '2.16rem',
        height: '2.16rem',
        borderRadius: '50%',
        transition: 'transform 0.5s',
        backgroundColor: theme === "dark" ? '#2A2A2A' : '#F3F4F6',
      }}
      whileTap={{ padding: 3 }}
      transition={{ duration: 0.2 }} 
      >

        <img 
                   src={theme === "dark" ?
                    Dark :
                    Light}
                    alt='light' 
                    style={{margin: '0.6rem',width: "100%"}}
                  />
                   
    </motion.div>
         
      
    
  );
};

export default ThemeToggle;