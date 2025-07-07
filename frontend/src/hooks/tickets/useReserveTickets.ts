import api from '@/api/api';
import { useMutation, useQueryClient,} from '@tanstack/react-query';



const fetchReserveTickets = async (event_id: string) => (await api.post(`/tickets/${event_id}/reserve`)).data;
 

export const useReserveTickets = () => {
  const queryClient = useQueryClient();
  const rechargeMutation = useMutation({
    mutationFn: (event_id: string) => fetchReserveTickets(event_id),
    
    onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['userTickets'] });
    },
  });

  
  return {
    reserve: rechargeMutation.mutateAsync,
    isReserving: rechargeMutation.isPending,
    reserveError: rechargeMutation.error,
    isReserveSuccess: rechargeMutation.isSuccess,
  };
};