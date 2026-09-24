import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { type ApprovalAction, decideMvp, generateMvp, getMvp } from './service'

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

export function useDecideMvp(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ version, action }: { version: number; action: ApprovalAction }) =>
      decideMvp(projectId, version, action),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['mvp', projectId] })
    },
  })
}
