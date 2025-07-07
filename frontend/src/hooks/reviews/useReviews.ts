import api from "@/api/api";
import { useQuery } from "@tanstack/react-query";



const fetchReviews = async (eventId: string | undefined, page: number, perPage: number) => {
    if (!eventId) return [];

    const { data } = await api.get(`/reviews/event/${eventId}/`, {
        params: { page, per_page: perPage }
    });

    return data;
};



const useReviews = (
  eventId: string | undefined,
  page: number = 1,
  perPage: number = 10
) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["reviews", eventId, page, perPage],
    queryFn: () => fetchReviews(eventId, page, perPage),
    enabled: !!eventId,
  });

  return {
    reviews: data,
    isLoading,
    error,
  };
};


export default useReviews;