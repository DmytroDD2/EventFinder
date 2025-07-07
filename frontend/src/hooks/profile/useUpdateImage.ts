import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '@/api/api';
import type { UserData } from '@/types/user';




const generateUrl = (userId: string | undefined): string => (
  userId
   ? `/users/admin/${userId}/image` 
    : '/users/image'
)
const useUpdateImage = (userId: string | undefined): {
  updateImage: (file: File) => void;
  uploadProgress: number;
  isLoading: boolean;
  error: Error | null;
} => {
  const queryClient = useQueryClient();
  const [uploadProgress, setUploadProgress] = useState<number>(0);

  const { mutate, isPending, error } = useMutation<UserData, Error, File>({
    mutationFn:async (imageFile: File) => {
      const formData = new FormData();
      formData.append('image', imageFile);
      
      return api.patch<UserData>(generateUrl(userId), formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            setUploadProgress(
              Math.round((progressEvent.loaded * 100) / progressEvent.total)
            );
          }
        }
      }).then(res => res.data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile', userId] });
      setUploadProgress(0);
    },
    onError: () => {
      setUploadProgress(0);
    },
  });

  return {
    updateImage: mutate,
    uploadProgress,
    isLoading: isPending,
    error,
  };
};


export default useUpdateImage