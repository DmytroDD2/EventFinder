

import { NavLink, useParams } from 'react-router-dom';
import InfoIcon from '@/assets/icons_svg/info.svg?react';
import FriendsIcon from '@/assets/icons_svg/friends.svg?react';
import TicketsIcon from '@/assets/icons_svg/tickets.svg?react';
import EventsIcon from '@/assets/icons_svg/events.svg?react';
import StarIcon from '@/assets/icons_svg/star.svg?react';
import NotificationsIcon from '@/assets/icons_svg/notifications.svg?react';
import * as motion from "motion/react-client"

import styles from './index.module.css';
import clsx from 'clsx';
import { useThemeStore } from '@/store/themeStore';


const HeaderProfile = () => {
   const { theme } = useThemeStore();
   const isDark = theme === "dark"
  const styleNav = ({ isActive }: { isActive: boolean }) => {
    
    return clsx(styles.nav_link,{
      [styles.active]: isActive && !isDark,
      [styles.dark_active]: isActive && isDark,
      [styles.inactive]: !isActive && !isDark,
      [styles.dark_inactive]: !isActive && isDark,
    });
  };


  let links = [
    { to: '/profile', label: 'Info', icon: InfoIcon },
    { to: '/profile/friends', label: 'Friends', icon: FriendsIcon },
    { to: '/profile/tickets', label: 'Tickets', icon: TicketsIcon },
    { to: '/profile/events', label: 'Events', icon: EventsIcon },
    { to: '/profile/reviews', label: 'Reviews', icon: StarIcon },
    { to: '/profile/notifications', label: 'Notifications', icon: NotificationsIcon },
  ];
  
  const { userId } = useParams();


  if (userId) {
    links = [
      {to: `/admin/${userId}`, label: 'Info', icon: InfoIcon },
      {to: `/admin/${userId}/friends/`, label: 'Friends', icon: FriendsIcon },
      {to: `/admin/${userId}/tickets/`, label: 'Tickets', icon: TicketsIcon },
      {to: `/admin/${userId}/events/`, label: 'Events', icon: EventsIcon },
      {to: `/admin/${userId}/notifications/`, label: 'Notifications', icon: NotificationsIcon },
      
    ]; 
  }
  return (
    <nav className={clsx(
      styles.profile_nav,
      isDark && styles.dark_profile_nav
      )}
    >
      <ul>
        
          {links.map(({ to, label, icon: Icon }) => (
            <motion.li key={to}
            whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }} >
              <NavLink
                to={to}
                end
                className={styleNav}
              >
                <Icon className={styles.icon} aria-label={label} />
                {label}
              </NavLink>
            </motion.li>
          ))}
     
      </ul>
    </nav>
  );
};

export default HeaderProfile;
