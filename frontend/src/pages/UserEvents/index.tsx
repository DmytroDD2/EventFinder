
import { useUserEvents } from "@/hooks/events/useUserEvents"
import styles from "./index.module.css"
import EventArticle from "@/components/EventArticle"
import Button from "@/components/Button"
import { useNavigate, useParams } from "react-router-dom"



const UserEvents = () => {
  const {userId} = useParams()
  const { userEvents, isLoading } = useUserEvents(userId)
  const navigate = useNavigate();
  if (isLoading) {
    return <div>Loading...</div>
  }
  const onClick = () => {
    
    navigate(
      userId
        ? `/admin/${userId}/events/create`
         :'/events/create'
    )
    
  }
  return (
    <div>
      <div className={styles.button_container}>
        <Button
         className={styles.button}
         onClick={onClick}
        >
          {"+ Create new event"}
        </Button>
      </div>
      <div className={styles.container}>
        {userEvents  && 
          <EventArticle
            events={userEvents}
            userId={userId}
          />
          }
      </div>
    </div>
  )
}

export default UserEvents