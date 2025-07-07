
import PinkPoint from '@/assets/icons/pink_point.png'
import PinkCalendar from '@/assets/icons/pink_calendar.png'
import Calendar from '@/assets/icons/calendar.png'
import Point from '@/assets/icons/point.png'
import styles from "./index.module.css"
import clsx from 'clsx'
import Button from '@/components/Button'
import { useReserveTickets } from '@/hooks/tickets/useReserveTickets'
import { useNavigate, useParams } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { transformDate } from '@/utils/data_format'


type InfoEventProps = {
    event_id: string
    description: string | null
    price: number 
    data: string | null
    venue: string | null
    dark: boolean
    creator: number
    
}

const InfoEvent = (event:InfoEventProps) => {
  const navigate = useNavigate()
  const {userId} = useParams()
  const {reserve} = useReserveTickets()

  const {user} = useAuthStore()
  const editMode = event.creator === user?.id || event.creator === Number(userId);


  const handleClick = async (event_id: string) => {
    if(editMode) {
      navigate(
        userId 
          ?`/admin/${userId}/events/edit/${event_id}`
           :`/events/edit/${event_id}`)
    };
    
    reserve(event_id)
  }
  return (
    <div className={clsx(styles.container, {[styles.light]: event.dark}) }>
        <section className={clsx(styles.description, {[styles.light]: event.dark})} >
            <h2>Event Information</h2>
            <p className={clsx(event.dark && styles.dark_description)}>{event.description}</p>
        </section>

        <section className={clsx(styles.price_label,{[styles.white_price_label]: !event.dark})} >

            <h2>Event Ditail</h2>

            <div>
                <img src={event.dark? PinkCalendar : Calendar} alt="calendar" />
                <div>
                    <h3>Date and Time</h3>
                    <p>
                      {event.data
                        ? transformDate(event.data)
                          : "still unknown"
                      }
                    </p>
                </div>
            </div>

            <div>
                <img src={event.dark? PinkPoint : Point} alt="point" />
                <div>
                    <h3>Location</h3>
                    <p>{event.venue}</p>
                </div>
                
            </div>
            
            <div className={styles.price}>
                <h3>Price</h3>
                <p>{event.price} $</p>
            </div>

            <Button
              className={styles.button}
              onClick={() => handleClick(event.event_id)}
            > 
                {editMode ? "Edit" : "Buy Ticket"}
            </Button>
           
            
        </section>

    </div>
  )
}

export default InfoEvent