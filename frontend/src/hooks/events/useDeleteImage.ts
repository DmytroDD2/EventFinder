
import api from '@/api/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const fetchDeleteImage = async ({
    eventId,
    imageId,
}: {
    eventId: string | number;
    imageId: string | number;
}) => {
    const response = await api.delete(`/events/${eventId}/images/${imageId}`, {
        
    });
    return response.data;
};

export const useDeleteImage = () => {
    const queryClient = useQueryClient();
    const deleteMutation = useMutation({
        mutationFn: fetchDeleteImage,
        onSuccess: (_data, variables) => {
            const { eventId } = variables;
     
            [['events'], ['userEvents'], ['eventDetails', String(eventId)]].forEach(key => {
                queryClient.invalidateQueries({ queryKey: key });
            });
        },
    });

    return {
        deleteImage: deleteMutation.mutateAsync,
        isDeleting: deleteMutation.isPending,
        deleteError: deleteMutation.error,
        isDeleteSuccess: deleteMutation.isSuccess,
    };
};
