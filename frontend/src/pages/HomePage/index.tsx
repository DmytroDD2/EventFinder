
import { useEvents } from "@/hooks/events/useEvents";
import EventArticle from "@/components/EventArticle";
import styles from "../HomePage/index.module.css"
import { useThemeStore } from "@/store/themeStore";
import clsx from "clsx";


const HomePage = () => {
    const events =  useEvents()
    const { theme } = useThemeStore();
    const check_dark = theme == 'dark'

    if (events.isLoading) {
      return <h1>Loading...</h1>
    }
    
    return (
    <div>
      <h1 className={clsx(check_dark && styles.dark)}>Current events</h1>
      <div className={styles.container}>
        {events?.data  && <EventArticle events={events.data}/>}
      
      </div>
    </div>
    );
  };
  
  export default HomePage;