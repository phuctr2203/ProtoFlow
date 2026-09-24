import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { generateMvp, getMvp } from './service'

export function useMvp(projectId: string) {
  return useQuery({
    queryKey: ['mvp', projectId],
    queryFn: () => getMvp(projectId),
    retry: false,
  })
}

export function useGenerateMvp(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => generateMvp(projectId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['mvp', projectId] })
    },
  })
}
