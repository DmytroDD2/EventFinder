import api from '@/api/api';
import { useQuery } from '@tanstack/react-query';

import { TicketsType } from '@/types/tickets';

const fetchUserTickets = async (userId: string | undefined) =>
  userId 
    ? (await api.get(`/tickets/admin/${userId}`)).data 
     : (await api.get('/tickets')).data;

const useTickets = (userId: string | undefined, enabled = true) => {

  const query = useQuery<TicketsType[]>({
    queryKey: ['userTickets', userId],
    queryFn: () => fetchUserTickets(userId),
    enabled,
    staleTime: 5 * 60 * 1000,
  });

 

  return {
    tickets: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
  };
};

export { useTickets };