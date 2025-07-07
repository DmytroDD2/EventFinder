import clsx from 'clsx';
import styles from './index.module.css';
import { useThemeStore } from '@/store/themeStore';

const Footer = () => {
  const { theme } = useThemeStore();
  return (
    <footer className={clsx(
      styles.footer,
       theme === "dark" && styles.dark_footer)}>
      <div className="">
        <p>&copy; 2023 Event App. Усі права захищені.</p>
      </div>
    </footer>
  );
};

export default Footer;