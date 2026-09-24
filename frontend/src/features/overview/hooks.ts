import { useQuery } from '@tanstack/react-query'

import { getOverview } from './service'

export function useOverview(projectId: string) {
  return useQuery({
    queryKey: ['overview', projectId],
    queryFn: () => getOverview(projectId),
    retry: false,
  })
}
