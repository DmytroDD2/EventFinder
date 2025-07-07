import api from '@/api/api';
import { useQuery } from '@tanstack/react-query';

import { Event } from '@/types/event';


const fetchUserEvents = async (userId: string | undefined) =>
  userId 
    ? (await api.get(`/events/admin/user/${userId}`)).data
     : (await api.get('/events/my')).data;

export const useUserEvents = (userId: string | undefined, enabled = true) => {

  const query = useQuery<Event[]>({
    queryKey: ['userEvents', userId],
    queryFn: () => fetchUserEvents(userId),
    enabled,
    staleTime: 5 * 60 * 1000,
  });

 

  return {
    userEvents: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
  };
};