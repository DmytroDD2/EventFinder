import styles from "./index.module.css"
import Button from "@/components/Button"
import { useNotifications } from "@/hooks/notifications/useNotifications"
import { useTickets } from "@/hooks/tickets/useTickets"
import { useState } from "react"
import DefaultImage from '@/assets/icons/default_image.png';
import clsx from "clsx"
import { useThemeStore } from "@/store/themeStore"

import { useNotification } from "@/hooks/notifications/useNotification"
import { useParams } from "react-router-dom"

type NotificationFileterType = "All notifications" | "Unread" | "Read"

const NotificationsPage = () => {
  const buttons: NotificationFileterType[] = ["All notifications", "Unread", "Read"]
  const {userId} = useParams()
  const [navButtons, setNavButtons] = useState<NotificationFileterType>("All notifications")
  const {notifications, isLoading} = useNotifications(userId)
  const getNotificationById = useNotification();
  const {tickets} = useTickets(userId);
  const { theme } = useThemeStore();
  const check_dark = theme == 'dark'
  const [openNotification, setOpenNotification] = useState<number[] | null>()
  
  if (isLoading) {
    return <h1>Loading...</h1>
  }
  if (!notifications) {
    return <h1>No notifications</h1>
  }

  const clickOpenNotification = (id: number) => {
    const notification = notifications.find((item) => item.id === id);
    if (notification) {
      getNotificationById(id);
      setOpenNotification((prev) => {
        if (prev && prev.includes(id)) {
          return prev.filter((item) => item !== id);
        } else {
          return [...(prev || []), id];
        }
      });
    }
  };

  

  const sortNotifications = () => {
    switch (navButtons) {
      case "All notifications":
        return notifications
      case "Unread":
        return notifications.filter((item) => !item.is_read)
      case "Read":
        return notifications.filter((item) => item.is_read)
      default:
        return notifications
    }
  }
  
  return (
    <div className={clsx(styles.container, check_dark && styles.dark)}>
      <div className={styles.navigation}>
        <h2>Notifications</h2>
        <div className={styles.buttons_container}>
          {
            buttons.map((item) => (
              <Button
               className={clsx(styles.buttons, navButtons === item && styles.active)}
               key={item}
               onClick={() => setNavButtons(item)}
              >{item}</Button>
            ))
          }
        </div>
      </div>
      <div className={styles.list_container}>
        {
          sortNotifications().map((item) => {
            const ticket = (tickets ?? []).find((e) => String(item.id) === String(e.ticket_id));
         
            return (
              <div
                key={item.id}
                className={clsx(
                  styles.notifications_container,
                  !item.is_read && navButtons === "All notifications" && styles.not_read_notification
                )}
                onClick={() => clickOpenNotification(item.id)}>
                

                <img className={styles.img_ivent}
                          src={
                            ticket && ticket.images && ticket.images[0]
                              ? (typeof ticket.images[0] === 'string'
                                  ? ticket.images[0]
                                  : ticket.images[0])
                              : DefaultImage
                          }
                          // className={styles.img}
                />
                {!item.is_read && <p className={styles.dot}></p>}  
                <div className={styles.notifications_info}>
                  
                  <h3>{ticket?.event_name}</h3>
                    {openNotification && openNotification.includes(item.id) ? (
                      <p className={styles.read}>{item.message}</p>
                    ) : (
                      <p>
                        {item.message.length > 30
                          ? item.message.slice(0, 80) + "..."
                          : item.message}
                      </p>
                    )}
                    
                </div>    
              </div>
            );
          })
        }
      </div>
    </div>
      
   
  )
}

export default NotificationsPage