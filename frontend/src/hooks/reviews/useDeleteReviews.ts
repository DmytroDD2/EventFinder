import api from '@/api/api';
import { useMutation, useQueryClient } from '@tanstack/react-query';



const fetchDeleteReviews = async (reviewId: string | number) => {
    const response = await api.delete(`/reviews/${reviewId}/delete`);
    return response.data;
};


const useDeleteReviews = () => {
    const queryClient = useQueryClient();
    const deleteMutation = useMutation({
        mutationFn: fetchDeleteReviews,
        onSuccess: () => {
            [['userReviews',]].forEach(key => {
                queryClient.invalidateQueries({ queryKey: key });
            });
        },
    });

    return {
        deleteReview: deleteMutation.mutateAsync,
        isDeleting: deleteMutation.isPending,
        deleteError: deleteMutation.error,
        isDeleteSuccess: deleteMutation.isSuccess,
    };
}

export default useDeleteReviews;