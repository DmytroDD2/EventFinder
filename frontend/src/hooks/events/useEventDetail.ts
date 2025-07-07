import api from '@/api/api';
import { useQuery } from '@tanstack/react-query';
import { Event } from '@/types/event';

const fetchEventDetail = async (eventId: string | undefined) =>
    (await api.get(`/events/${eventId}`)).data;

export const useEventDetail = (eventId: string | undefined, enabled = true) => {
    const query = useQuery<Event>({
        queryKey: ['eventDetails', eventId],
        queryFn: () => fetchEventDetail(eventId),
        enabled: enabled && !!eventId,
        staleTime: 5 * 60 * 1000,
    });

    return {
        event: query.data,
        isLoading: query.isLoading,
        isError: query.isError,
        refetch: query.refetch,
    };
};
