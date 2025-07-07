
import Profile from '@/components/Profile'
import styles from './ProfileLayout.module.css';
import { useLocation, useOutlet } from 'react-router-dom';
import HeaderProfile from '@/components/HeaderProfile';
import { AnimatePresence, motion } from 'framer-motion';
import {useMemo, useRef} from 'react';



const routeOrder = [
    '/profile',
    '/profile/friends',
    '/profile/tickets',
    '/profile/events',
    '/profile/reviews',
    '/profile/notifications'
  ];


const variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 100 : -100,
    opacity: 0
  }),
  center: {
    x: 0,
    opacity: 1
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 100 : -100,
    opacity: 0
  })
};

const ProfileLayout = () => {
  const location = useLocation();
  const outlet = useOutlet();
  const prevIndex = useRef(0);

  const direction = useMemo(() => {
    const newIndex = routeOrder.indexOf(location.pathname);
    const prev = prevIndex.current;
   
    const dir = newIndex > prev ? 1 : -1;
    prevIndex.current = newIndex;
    return dir;
  }, [location.pathname]);


  return (
    <div className={styles.container}>
      <Profile />
      <HeaderProfile />
      <AnimatePresence initial={false} >
        <motion.div
          key={location.pathname}
          custom={direction}
          variants={variants}
          initial="enter"
          animate="center"
          exit="exeit"
          transition={{
            x: { type: "spring", stiffness: 400, damping: 30 },
            opacity: { duration: 0.2 }
          }}
        >
          {outlet}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default ProfileLayout;

