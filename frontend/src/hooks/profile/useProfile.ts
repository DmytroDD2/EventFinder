import api from '@/api/api';
import { useMutation, useQuery, useQueryClient} from '@tanstack/react-query';
import { UserData } from '@/types/user';

const fetchProfile = async (userId: string | undefined) =>
  userId 
    ? (await api.get(`/users/admin/${userId}`)).data 
    :(await api.get('/users')).data;



export const useProfile = (userId: string | undefined = undefined, enabled = true) => {
  
  const query = useQuery<UserData>({
    queryKey: ['profile', userId],
    queryFn: () => fetchProfile(userId),
    enabled,
    staleTime: 5 * 60 * 1000,
  });
  
  const queryClient = useQueryClient();

  const rechargeMutation = useMutation({
    mutationFn: (amount: number) => 
      userId 
        ? api.post(`/users/admin/${userId}/recharge`, { amount })
        : api.post('users/recharge', { amount }),
      
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["profile", userId]} );;
    },
  });

  return {
    profile: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    rechargeBalance: rechargeMutation.mutateAsync,
    isRecharging: rechargeMutation.isPending,
    rechargeError: rechargeMutation.error,
    іsRechargeSuccess: rechargeMutation.isSuccess,
    refetch: query.refetch,
  };
};