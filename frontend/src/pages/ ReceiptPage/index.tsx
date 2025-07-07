
import SuccessfullSvg from'@/assets/icons_svg/successful.svg?react'
import styles from './index.module.css'
import DateTime from '@/components/DateTime';
import Button from '@/components/Button';
import WalletSvg from '@/assets/icons_svg/wallet.svg?react';
import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';
type BalanceType = {
  balance: number;
  charge: number;
  isDark: boolean;
  userId?: string;
}



const ReceiptPage = (number: BalanceType) => {
  const navigate = useNavigate();
  const handleBackToWallet = () => {
    navigate( 
      number.userId
    ? `/admin/${number.userId}`
     : '/profile', { replace: true }
    )
    
  }
  return (
   
        <div className={clsx(styles.container, number.isDark && styles.dark)}>
            <SuccessfullSvg className={styles.icon}/>
            <h2>Payment Successful!</h2>
            <p className={styles.subtext}>Your account has been recharged</p>

            <div className={styles.receipt}>
              <div className={styles.amount}>
                <span>Amount Added:</span>
                <strong>${number.charge.toFixed(2)}</strong>
              </div>
              <div className={styles.balance}>
                <span>New Balance:</span>
                <strong>${number.balance.toFixed(2)}</strong>
              </div>
              <div className={styles.transaction}>
                <span className={styles.span_name} >Transaction ID:</span>
                <span >#TRX123456</span>
              </div>
              <div className={styles.date}>
                <span className={styles.span_name} >Date & Time:</span>
                <DateTime />
              </div>
            </div>
            <Button className={styles.button} onClick={handleBackToWallet}>
              <WalletSvg />
              Back to Wallet
            </Button>
        </div>

 
  
  )
}

export default ReceiptPage