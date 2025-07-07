
import { useMutation} from '@tanstack/react-query';
import api from '@/api/api';
import type { UserData } from '@/types/user';
import { TypeInput } from '@/utils/types/submit';
import { useAuthStore } from '@/store/authStore';

const generateChangeUrl = (userId: string | undefined) => (
   userId 
    ? `/users/admin/${userId}/password` 
      : '/users/password'
);
export const useChangePassword = (type: TypeInput, userId: string | undefined): {
  changePassowrd: (data: FormData) => Promise<void>;
  isLoading: boolean;
  error: Error | null;
} => {
  const route =
    type === 'change'
      ? generateChangeUrl(userId)
      : type === 'registration'
      ? '/users/register'
      : '/users/password-reset';
  
  const { mutateAsync, isPending, error } = useMutation<UserData, Error, FormData>({
    mutationFn: async (data: FormData) => {
      const response = await api[type === 'registration' ? 'post' : 'patch']<UserData>(route, data, {
      headers: {
        'Content-Type': 'application/json',
        accept: 'application/json',
      },
      });
      
      if (type === 'registration' && response.status === 201) {
        
      useAuthStore.getState().login(
        data.get('username') as string,
        data.get('password') as string)
      }
      
      return response.data;
    },
    });

  return {
    changePassowrd: async (data: FormData) => {
      await mutateAsync(data);
    },
    isLoading: isPending,
    error,
  };
};

export default useChangePassword