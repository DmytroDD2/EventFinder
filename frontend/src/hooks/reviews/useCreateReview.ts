import api from '@/api/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';

type CreateReviewType = {
    eventId: string | undefined;
    rating: number;
    description: string;
};



const fetchCreateReview = async ({ eventId, rating, description }: CreateReviewType) => {
    
    const integerRating = Math.floor(rating);

    const response = await api.post(
        `/reviews/event/${eventId}/create-review`,
        { rating: integerRating, description: description },
        {
            headers: {
                'Content-Type': 'application/json',
                 accept: 'application/json',
            }
        }
    );
    return response.data;
};

const useCreateReview = () => {
    const queryClient = useQueryClient();
    const createMutation = useMutation({
        mutationFn: fetchCreateReview,
        onSuccess: (_data, variables) => {
            queryClient.invalidateQueries({ queryKey: ['reviews', variables.eventId] });
        },
    });

    return {
        createReview: createMutation.mutateAsync,
        isCreating: createMutation.isPending,
        createError: createMutation.error,
        isCreateSuccess: createMutation.isSuccess,
    };
};

export default useCreateReview;