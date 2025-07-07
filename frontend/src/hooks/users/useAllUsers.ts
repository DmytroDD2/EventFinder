import { useQuery } from "@tanstack/react-query";
import api from "@/api/api";
import { FriendType } from "@/types/friends";

const fetchAllUsers = async (): Promise<FriendType[]> => 
  (await api.get("/users/all-users")).data;

export const useAllUsers = (enabled = true) => {
  const query = useQuery<FriendType[]>({
    queryKey: ["all-users"],
    queryFn: fetchAllUsers,
    enabled,
    staleTime: 5 * 60 * 1000,
  });
 
  return {
    users: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    refetchUsers: query.refetch,
  };
};