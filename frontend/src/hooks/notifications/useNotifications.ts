import api from '@/api/api';
import NotificationType from '@/types/notification';
import { useQuery } from '@tanstack/react-query';



const fetchUserNotifications = async (userId: string | undefined) =>
  userId

    ? (await api.get(`/notifications/admin/${userId}`)).data
     :(await api.get('/notifications')).data;

export const useNotifications = (userId: string | undefined, enabled = true) => {

  const query = useQuery<NotificationType[]>({
    queryKey: ['notifications'],
    queryFn: () => fetchUserNotifications(userId),
    enabled,
    staleTime: 5 * 60 * 1000,
  });



  return {
    notifications: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
  };
};