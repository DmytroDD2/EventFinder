import api from '@/api/api';
import NotificationType from '@/types/notification';
import { useQueryClient } from '@tanstack/react-query';

const fetchNotificationById = async (notificationId: number): Promise<NotificationType> => {
  const response = await api.get(`users/notifications/${notificationId}`);
  return response.data;
};

export const useNotification = () => {
  const queryClient = useQueryClient();

  const getNotificationById = (notificationId: number) => {
    return queryClient
      .fetchQuery<NotificationType>({
        queryKey: ['notification', notificationId],
        queryFn: () => fetchNotificationById(notificationId),
      })
      // .then((data) => {
      //   [['notifications']].forEach(key => {
      //     queryClient.invalidateQueries({ queryKey: key });
      //   });
      //   return data;
      // });
    
  };
  
  return getNotificationById;
};




// const fetchUserNotifications = async ({ queryKey }: { queryKey: readonly unknown[] }) => {
//   const [, id] = queryKey as [string, number];
//   return (await api.get(`/users/notifications/${id}`)).data;
// };

// export const useNotifications = (userId: number, enabled = true) => {

//   const query = useQuery<NotificationType[]>({
//     queryKey: ['notifications', userId],
//     queryFn: fetchUserNotifications,
//     enabled,
//     staleTime: 5 * 60 * 1000,
//   });



//   return {
//     notifications: query.data,
//     isLoading: query.isLoading,
//     isError: query.isError,
//     refetch: query.refetch,
//   };
// };