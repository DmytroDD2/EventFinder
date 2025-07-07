import { useProfile } from '@/hooks/profile/useProfile';
import styles from './index.module.css';

import { UserAvatar } from '../UserAvatar';
import Button from '../Button';
import { useThemeStore } from '@/store/themeStore';
import clsx from 'clsx';
import WalletImage from "@/assets/icons_svg/wallet.svg?react";
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { usePatchUserRole } from '@/hooks/admin/usePomouteAdmin';




const Profile = () => {
  const navigate = useNavigate();
  const { userId } = useParams();
  const location = useLocation();
  const admin = location.pathname.includes('/admin');
  const { profile, isLoading } = useProfile(userId);
  const {patchUserRole}  = usePatchUserRole()
  
  const isAdmin = profile?.role === 'admin';

  const {theme} = useThemeStore();
  const isDark = theme === 'dark'

  if (!profile || isLoading) return <div>Loading...</div>;

  const onClick = () => {
    navigate( userId ? `/admin/${userId}/recharge` :'/recharge');
  }
  
  return (
    <div className={styles.container}>

       <UserAvatar user={{
          email: profile.email,
          firstName: profile.first_name,
          lastName: profile.last_name,
          url: profile.profile_picture
        }}
        className={styles.avatar}
        />

      <div className={clsx(styles.info, {[styles.dark]: isDark})}>
        <p className={styles.name}>{profile.first_name} {profile.last_name}</p>
        <p className={styles.email}>{profile.email}</p>
        <div className={styles.balance_with_button}>
          <div className={styles.balance}>
            <WalletImage />
            <p>${profile.balance.toFixed(2)}</p>
          </div > 
          <div className={styles.buttons}>
            <Button
              onClick={onClick}
              className={styles.button}
            >
              Recharge balance
            </Button>
            {
              admin &&  userId &&
                <Button
                  className={styles.button}
                  onClick={() => patchUserRole(userId)}
                >
                  {isAdmin ? 'Remove admin' :'Make admin'} 
                </Button>
              
            }
            
          </div>
        
        </div>
      </div>
    </div>
  )
}

export default Profile