import api from '@/api/api';
import { FriendType, } from '@/types/friends';


import { useQuery, useQueryClient } from "@tanstack/react-query";


const fetchFriends = async (userId: string | undefined): Promise<FriendType[]> =>
  userId
    ? (await api.get(`/users/friends/${userId}`)).data
    :(await api.get("/users/friends")).data;

export const useFriends = (userId: string | undefined, enabled = true) => {
  const queryClient = useQueryClient();

  const query = useQuery<FriendType[]>({
    queryKey: ["friends", userId],
    queryFn: () => fetchFriends(userId),
    enabled,
    staleTime: 5 * 60 * 1000,
  });

  const buildUrl = (action: "add" | "remove", friendId: number) => {
    return userId
      ? `/users/friends/admin/${userId}/${friendId}/${action}`
      : `/users/friends/${friendId}/${action}`;
  };

  const updateFriends = (url: string, key = ["friends", userId]) =>
    api.post(url).then(() => queryClient.invalidateQueries({ queryKey: key }));

  const addFriend = (friendId: number) => updateFriends(buildUrl("add", friendId), userId ? ["friends", userId] : ["friends"]);
  
  const removeFriend = (friendId: number) =>
    api.delete(buildUrl("remove", friendId)).then(() =>
      queryClient.invalidateQueries({ queryKey: userId ? ["friends", userId] : ["friends"] })
    );

  return {
    friends: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
    addFriend,
    removeFriend,
  };
};
