import api from '@/api/api';
import { EventFormType } from '@/pages/CreateEventPage';

import { useMutation, useQueryClient,} from '@tanstack/react-query';


const genereteUrl = (userId: string | undefined) => {
    return userId
        ? `/events/admin/user/${userId}/create-event`
        : `/events/create-event`;
}
    


const fetchCreateEvent = async (data: EventFormType, eventId: string | undefined) => {
    const formData = new FormData();

   
    if (Array.isArray(data.images)) {
        data.images.forEach((img) => {
            formData.append('images', img as Blob);
        });
    } else if (data.images) {
        formData.append('images', data.images);
    }
    
    const response = await api.post(genereteUrl(eventId), formData, {
        params: {
            name: data.name,
            category: data.category,
            venue: data.venue,
            description: data.description,
            price: data.price,
            total_tickets: data.total_tickets,
            data: data.data 
        },
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const useCreateEvent = (userId: string | undefined) => {
    const queryClient = useQueryClient();
    const rechargeMutation = useMutation({
        mutationFn: (data: EventFormType) => fetchCreateEvent(data, userId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['userEvents'] });
        },
    });


  
  return {
    createEvent: rechargeMutation.mutateAsync,
    isCreating: rechargeMutation.isPending,
    createError: rechargeMutation.error,
    isCreateSuccess: rechargeMutation.isSuccess,
  };
};