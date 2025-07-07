// src/hooks/useEvents.ts

import api from '@/api/api';
import { useQuery } from '@tanstack/react-query';


const fetchEvents = async () => {
  const response = await api.get('/events?page=1&per_page=10');
  return response.data;
};

const fetchEventsFilter = async (params?: string) => {
  const response = await api.get(`/events/filter?${params}`);
  return response.data;
};

type TepeHook = {
  filter?: string;
}

export const useEvents = (event?: TepeHook) => {
  const query = event?.filter ? () => fetchEventsFilter(event?.filter) : fetchEvents;
  const keys = event?.filter ? ['filter', 'events', event.filter] : ['events'];

  return useQuery({
    queryKey: keys,
    queryFn: query,
    staleTime: 5 * 60 * 1000,
    select: (data) => {
      return data;
    },
  });
};
