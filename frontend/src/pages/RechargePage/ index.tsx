import Button from "@/components/Button"
import styles from "./index.module.css"
import clsx from "clsx"
import { useState } from "react";
import Wallet from "@/assets/icons_svg/wallet.svg?react";
import { useThemeStore } from "@/store/themeStore";
import { useProfile } from "@/hooks/profile/useProfile";
import { ClipLoader } from "react-spinners";
import ReceiptPage from "../ ReceiptPage";
import { useNavigate, useParams } from "react-router-dom";


const  RechargePage = () => {
    
    const {theme} = useThemeStore();
    const isDark = theme === 'dark'
    const {userId} = useParams();
    const navigate = useNavigate();
    const {
      rechargeBalance,
      isRecharging,
      profile,
      іsRechargeSuccess,
      refetch
    } = useProfile(userId, false);

    const [amount, setAmount] = useState(0);
    

   const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      rechargeBalance(amount);
      refetch()
    };

    const handleCustomAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const amount = parseFloat(e.target.value);
      setAmount(amount);

    };

    const handleCustomAmountChangeButton = (amount: number) => {
      setAmount(amount);
    };

    const handleCancel = () => {
      setAmount(0);
      navigate("/profile");
    };

  return (
    <div className={clsx(styles.container, isDark && styles.dark)}>
        {
         іsRechargeSuccess && profile
          ? <ReceiptPage
              isDark={isDark}
              balance={profile.balance}
              charge={amount}
              userId={userId}
            />
          : 
          <div className={styles.content}>
              
              <div className={styles.header}>
                  <Wallet className={styles.wallet_svg}/>
                  <h2>Recharge Balance</h2>
                  <p >Add funds to your account</p>
              </div>
              <div className={styles.current_balance}>
              {isRecharging ?
                  <ClipLoader color="#FF4F81" />
                  :
                  <><p>Current Balance</p> ${profile?.balance.toFixed(2)}</>
              }
              </div>
              <h3>Select amount:</h3>
              <div className={styles.amount_buttons}>
                {[10, 20, 50, 100].map((amount) => (
                  <Button
                    key={amount}
                    type="button"
                    className={styles.amountButton}
                    onClick={() => handleCustomAmountChangeButton(amount)}
                  >
                    {amount}$
                  </Button>
                ))}
              </div>
              
              <form onSubmit={handleSubmit} className={styles.form}>
                  <fieldset className={styles.fieldset}>
                  <label htmlFor="custom-amount">Custom amount:</label>
                  <input
                      type="number"
                      id="custom-amount"
                      min="5"
                      step="0.01"
                      value={amount.toString()}
                      onChange={handleCustomAmountChange}
                      placeholder="$ Enter amount"
                  />
                  </fieldset>
                  <div className={styles.buttons}>
                      <Button
                      className={styles.cancel}
                      type="button" 
                      onClick={handleCancel}
                      >
                        Cancel
                      </Button>

                      <Button
                      className={styles.recharge}
                      type="submit"
                      >
                        Recharge
                      </Button>
                  </div>
              </form>
              
          </div>}
      </div>
  )
}

export default  RechargePage