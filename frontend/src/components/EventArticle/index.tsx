
import { Event } from '@/types/event'
import { useThemeStore } from '@/store/themeStore';
import styles from "./index.module.css"
import clsx from 'clsx';
import { useNavigate } from 'react-router-dom';
import DefaultImage from '@/assets/icons/default_image.png';
import Button from '../Button';
import { TicketsType } from '@/types/tickets';
import { transformDate } from '@/utils/data_format';

const EventArticle = ({ events, userId }: { events: Array<Event | TicketsType>, userId?: string | undefined}) => {
  const { theme } = useThemeStore();
  const check_dark = theme === 'dark';
  const navigate = useNavigate();

  const handleClick = (event: Event | TicketsType) => {
    const id = 'id' in event ? event.id : event.event_id;
    navigate(
      userId 
        ? `/admin/${userId}/events/${id}` 
         :`/events/${id}`);
  };

  const isEvent = (item: Event | TicketsType): item is Event => {
    return 'venue' in item;
  };
  // if (!events) {
  //   return <div className={styles.no_events}>No events found</div>;
  // }
  return (
    <>
      {events.map((event) => (
        <article
          key={'id' in event ? event.id : event.ticket_id}
          className={clsx(styles.article, check_dark && styles['black-article'])}
        >
          <img
            src={typeof event.images?.[0] === 'string' ? event.images?.[0] : event.images?.[0]?.image_url || DefaultImage}
            alt={'name' in event ? event.name : event.event_name}
            className={styles.img}
          />
          <div className={styles.container}>
            <h2 className={clsx(styles.items, styles.event_name)}>
              {'name' in event ? event.name : event.event_name}
            </h2>
            <p className={styles.items}>
              {event.data ?
              transformDate(event.data) : 'still unknown'}
            </p>
            {isEvent(event) && <p className={styles.items}>{event.venue}</p>}
          </div>
          <Button className={styles.button} onClick={() => handleClick(event)}>
            Details
          </Button>
        </article>
      ))}
    </>
  );
};

export default EventArticle