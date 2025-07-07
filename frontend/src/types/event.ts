import { ImageType } from "./image";

type Category = "Sport" | "Music"  | "Technology" | "Other" | "Arts";

type Image = {
  id: number,
  event_id: number,
  image_url: string
}
type Event  = {
    id: string;
    name: string; 
    images: Array<ImageType> | undefined;
    description: string;
    price: number;
    total_tickets: number;
    data: string | null;
    category: Category;
    venue: string
    creator: number
  }
  
type EventState = {
    events: Event[];
    loading: boolean;
    error: string | null;
    fetchEvents: () => Promise<void>;
    addEvent: (event: Event) => void;
  }
  
export type { Event, EventState, Category, Image };