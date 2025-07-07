import api from '@/api/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';

type AddImagesParams = {
    eventId: number | string;
    images: File[];
  
};

const fetchAddEventImages = async ({ eventId, images}: AddImagesParams) => {
    const formData = new FormData();
    images.forEach((img) => {
        formData.append('images', img);
    });
    console.log("form dataa", formData);


    
    const response = await api.post(
        `/events/events/${eventId}/images/`,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data',
                'accept': 'application/json',
            },
        }
    );

    return response.data;
};

export const useAddEventImages = () => {
    const queryClient = useQueryClient();
    const mutation = useMutation({
        mutationFn: fetchAddEventImages,
        onSuccess: (_data, variables) => {
           
            const { eventId } = variables;
        
            [['events'], ['userEvents'], ['eventDetails', eventId.toString()]].forEach(key => {
                queryClient.invalidateQueries({ queryKey: key });
            });
        },
    });

    return {
        addImages: mutation.mutateAsync,
        isAdding: mutation.isPending,
        addError: mutation.error,
        isAddSuccess: mutation.isSuccess,
    };
};
