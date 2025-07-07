import { useTickets } from "@/hooks/tickets/useTickets";
import styles from "./index.module.css"

import EventArticle from "@/components/EventArticle";
import { useParams } from "react-router-dom";
import { useThemeStore } from "@/store/themeStore";
import clsx from "clsx";



const TicketsPage = () => {
  const {userId} = useParams()
  const {tickets, isLoading} =  useTickets(userId)
  const {theme} = useThemeStore()
  const check_dark = theme === 'dark'

  if (isLoading) {
    return <h1>Loading...</h1>
  }

 
  return (
    <div className={clsx(styles.container, check_dark && styles.dark)}>
      {!tickets
       ? <h1 className={styles.no_tickets}>No tickets found</h1>
        : <EventArticle events={tickets}/>
        }
     
    </div> 
  )
}

export default TicketsPage