
import styles from "./index.module.css"
import { useParams } from 'react-router-dom'
import TitleEvent from './TitleEvent'
import ImageEvent from './ImageEvent'
import InfoEvent from './InfoEvent'
import { useThemeStore } from '@/store/themeStore'
import { useEventDetail } from "@/hooks/events/useEventDetail"

import CreateReview from "@/components/CreateReview"
import ReviewArticle from "@/components/ReviewArticle"
import useReviews from "@/hooks/reviews/useReviews"



const EventDetail = () => {
  const { eventId } = useParams();
  const {event, isLoading} =  useEventDetail(eventId);
  const {reviews, isLoading: reviewsLoading} = useReviews(eventId);
  
  const { theme } = useThemeStore();
  const dark = theme === "dark"

  if (isLoading || !event) {
    return <div>Loading...</div>
  }

  
  
  return (
    <div className={styles.container}>
      
      <TitleEvent name={event.name} date={event.data} vanue={event.venue} dark={dark}/>
      <ImageEvent images={event.images ?? []}></ImageEvent>
      <InfoEvent
        description={event.description}
        price={event.price}
        data={event.data}
        venue={event.venue}
        dark={dark}
        event_id={event.id}
        creator={event.creator}
         /> 
         
      <CreateReview dark={dark }/>
      {reviewsLoading 
       ? <p>Loading...</p>
        : <ReviewArticle reviews={reviews} dark={dark}/>
      }
      
    </div>
  )
}

export default EventDetail