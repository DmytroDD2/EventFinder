import { UsersType } from "@/pages/UsersPage";
import { FriendType } from "@/types/friends";
import { useMemo } from "react";

type typeFilterUsers = {
  searchQuery: string;
  friends: FriendType[] | undefined;
  users?: FriendType[];
  typeUser:  UsersType["usersType"] | undefined;
}


const useFilteredFriends = ({ friends, searchQuery, typeUser, users = [] }: typeFilterUsers) => {
  return useMemo(() => {
    const query = searchQuery.toLowerCase();

    const matchesQuery = (user: FriendType) =>
      user.first_name.toLowerCase().includes(query) ||
      user.last_name.toLowerCase().includes(query) ||
      user.username.toLowerCase().includes(query);

    if (typeUser === "admin") {
      return users.filter(matchesQuery);
    }

    // if (!friends) return [];

    if (typeUser === "users") {
      if (!friends) return users.filter(matchesQuery);
      const friendIds = new Set(friends.map(friend => friend.id));
      return users.filter(user => !friendIds.has(user.id) && matchesQuery(user));
    }

    if(!friends) return []
    const friendIds = new Set(friends.map(friend => friend.id));
    return users.filter(user => friendIds.has(user.id) && matchesQuery(user));

  }, [friends, searchQuery, users, typeUser]);
};

export { useFilteredFriends };