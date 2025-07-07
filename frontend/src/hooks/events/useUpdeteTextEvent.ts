
import api from '@/api/api';
import { EventFormType } from '@/pages/CreateEventPage';
import { Event } from '@/types/event';
import { useMutation, useQueryClient } from '@tanstack/react-query';

type EditEventParams = {
    name?: string;
    category?: string;
    venue?: string;
    description?: string;
    price?: number;
    total_tickets?: number;
    data?: string;
};

const fetchUpdateTextEvent = async ({
    id,
    data,
    event,
}: {
    id: string | number;
    data: EventFormType;
    event: Event;
}) => {
    const formData = new FormData();
    const params: EditEventParams = {};

    if (data.name !== event?.name) params.name = data.name;
    if (data.category !== event?.category) params.category = data.category;
    if (data.venue !== event?.venue) params.venue = data.venue;
    if (data.description !== event?.description) params.description = data.description;
    if (data.price !== event?.price) params.price = data.price;
    if (data.total_tickets !== event?.total_tickets) params.total_tickets = data.total_tickets;
    if (data.data !== event?.data) params.data = data.data ;

    const response = await api.put(`/events/${id}/edit`, formData, {
        params,

        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const useUpdateTextEvent = () => {
    const queryClient = useQueryClient();
    const updateMutation = useMutation({
        mutationFn: fetchUpdateTextEvent,
        onSuccess: (_data, variables) => {
           
            const { id } = variables;
        
            [['events'], ['userEvents'], ['eventDetails', id]].forEach(key => {
                queryClient.invalidateQueries({ queryKey: key });
            });
        },
    });

    return {
        updateText: updateMutation.mutateAsync,
        isUpdating: updateMutation.isPending,
        updateError: updateMutation.error,
        isUpdateSuccess: updateMutation.isSuccess,
    };
};