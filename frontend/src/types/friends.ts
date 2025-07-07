
type FriendType = {
  id: number;
  username: string;
  profile_picture: string;
  email: string;
  first_name: string;
  last_name: string;
}

type queryTypes = "users" | "friends" ;


export type {FriendType, queryTypes};