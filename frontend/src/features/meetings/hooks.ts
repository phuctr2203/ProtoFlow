import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { listMeetings, simulateMeeting } from './service'

export function useMeetings(projectId: string) {
  return useQuery({
    queryKey: ['meetings', projectId],
    queryFn: () => listMeetings(projectId),
  })
}

export function useSimulateMeeting(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (fixture: string) => simulateMeeting(projectId, fixture),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['meetings', projectId] })
    },
  })
}
