import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/api/api';
import type { UserData } from '@/types/user';

export const useUpdateProfile = (): {
  updateProfile: (data: FormData) => void;
  isLoading: boolean;
  error: Error | null;
} => {
  const queryClient = useQueryClient();

  const { mutate, isPending, error } = useMutation<UserData, Error, FormData>({
    mutationFn: (data: FormData) =>
      api.put<UserData>('/users/change', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'accept': 'application/json',
        },
      }).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },
  });

  return {
    updateProfile: mutate,
    isLoading: isPending,
    error,
  };
};