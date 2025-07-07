import api from "@/api/api";
import { TypeUserReview } from "@/types/reviews";
import { useQuery } from "@tanstack/react-query";


type userReviewParams = {
  userId?: string | undefined;
  page?: number;
  perPage?: number;
  enabled?: boolean;
}



const fetchUserReviews = async ({userId, page, perPage}: userReviewParams): Promise<TypeUserReview[]> => {
    const url = userId
        ? `/reviews/admin/${userId}/reviews`
        : `/reviews/my`;

    const params = { page, per_page:perPage };
    const response = await api.get(url, { params });
    return response.data;
};

const useUserReviews = ({userId, page = 1, perPage = 10, enabled=false}: userReviewParams) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["userReviews", userId, page, perPage],
    queryFn: () => fetchUserReviews({ userId, page, perPage }),
    enabled: !!userId || enabled,
  });

  return {
    userReviews: data,
    isLoading,
    error,
  };
};

export default useUserReviews