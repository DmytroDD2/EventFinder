import { NavLink } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import styles from './index.module.css';
import ThemeToggle from '../ThemeToggle';
import { useThemeStore } from '@/store/themeStore';
import clsx from 'clsx';
import { useProfile } from '@/hooks/profile/useProfile';

const Header = () => {
  const { theme } = useThemeStore();
  const { isAuthenticated, logout} = useAuthStore();
  const {profile} = useProfile()

  const styleNav = ({ isActive }: { isActive: boolean }, label: string) => {
    const dark = theme === 'dark';
    return clsx({
      [styles.active]: isActive && !dark,
      [styles.dark_active]: isActive && dark,
      [styles.inactive]: !isActive && !dark,
      [styles.dark_inactive]: !isActive && dark,
      [styles.adminLink]: label === 'Admin',
      [styles.adminActive]: label === 'Admin' && isActive,
   
    });
  };

 
  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/events', label: 'Events' },
    { to: '/profile', label: 'Profile' },

  ];
 
  if (profile?.role === 'admin') {
    navLinks.push({ to: '/admin', label: 'Admin' });
  }

  return (
    <header className={clsx(styles.head_st, theme === 'dark' && styles.dark_h)}>
      <nav className={styles.nav}>
        <p className={clsx( theme === 'dark' ? styles.white_logo : styles.logo, styles.logo_m,)}>
          EventSphere
        </p>

        <div>
          {navLinks.map(({ to, label }) => (
            <NavLink key={to} to={to} className={(navProps) => styleNav(navProps, label)}>
          
              {label === 'Admin'
               ? <span className={styles.adminBadge}>Admin</span>
                : <span>{label}</span>
              }
            </NavLink>
          ))}
        </div>
      </nav>

      <div className={styles.auth}>
        <ThemeToggle />
        {isAuthenticated ? (
          <>
            <button onClick={logout} className={styles.logout}>
              out
            </button>
          </>
        ) : (
          <>
            <NavLink
              to="/login"
              className={theme === 'dark' ? styles.dark_login : styles.login}
            >
              sign in
            </NavLink>

            <NavLink to="/register" className={styles.signup}>
              sign up
            </NavLink>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;
