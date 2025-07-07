
import { Category } from "./event";

type UserRole = 'admin' | 'user';

type UserLog = {
    password: string;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    role: UserRole;
    password_reset_question: string;
    
};



type UserData = {
  id: number;
  first_name: string;
  last_name: string;
  username: string;
  profile_picture: string | "string";
  email: string;
  role: UserRole;
  balance: number;
}

type EventImageBase = {
  id: number;
  event_id: number;
  image_url: string;
}
type ResponseEvent = {
  category: Category | null;
  name: string | null;
  venue: string | null;
  description: string | null;
  price: number | null;
  total_tickets: number | null;
  data: string | null; // date-time
  id: number;
  images: EventImageBase[];
}

type BaseResponseTickets = {
  ticket_id: number;
  event_id: number;
  event_name: string;
  data: string | null; // date-time
  creator: string;
  description: string | null;
  images: (string | null)[];
}

type BaseResponseFriendsTickets = BaseResponseTickets & {
  profile_picture: string | null;
  friend_id: number;
  friend_name: string;
};



// Додаткові типи, які можуть знадобитись
export interface BaseReview {
  rating: number; // 1-5
  description: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type?: string; // default "bearer"
}





export type { 
    UserRole,
    UserLog,
    UserData,
    EventImageBase,
    ResponseEvent,
    BaseResponseTickets,
    BaseResponseFriendsTickets 
};