import styles from "./index.module.css"

import { useParams, useSearchParams } from "react-router-dom";
import { useEvents } from "@/hooks/events/useEvents";
import { useThemeStore } from "@/store/themeStore";

import EventFilter from "./EventFilter";
import EventArticle from "@/components/EventArticle";
import clsx from "clsx";
import PaginationControls from "@/components/PaginationControls";



function EventsPage() {
  const [searchParams] = useSearchParams();
  let totaEvents = null
  const { eventId } = useParams();
  const currentPage = parseInt(searchParams.get('page') || '1', 10);
  
  if (!totaEvents){
    searchParams.set('totalCount', 'true');
  }

  const events = useEvents({filter: searchParams.toString()});
  
  const data = events.data?.items || events.data;
  totaEvents = events.data?.totalCount;

  const totalPages = Math.ceil(totaEvents / 10);

  const { theme } = useThemeStore();
  const check_dark = theme == 'dark'

  if (events.isLoading) {
    return <h1>Loading...</h1>
  }

  
  return (
    
    <div  > 
         
          <h1 className={clsx(styles.title, check_dark && styles.dark)}>Current events</h1>
          <EventFilter dark={check_dark}/>
          <div className={clsx(styles.container, "scroll-wrapper")}>
            {events?.data && <EventArticle userId={eventId} events={data}/>}
          </div>

        {totalPages > 1 && (
        <PaginationControls 
          currentPage={currentPage}
          totalPages={totalPages}
          dark={check_dark}
        />
      )}

    </div>
  );
}

export default EventsPage;