import { useQuery } from '@tanstack/react-query'

import { getIntelligence } from './service'

export function useIntelligence(meetingId: string) {
  return useQuery({
    queryKey: ['intelligence', meetingId],
    queryFn: () => getIntelligence(meetingId),
    retry: false,
  })
}
