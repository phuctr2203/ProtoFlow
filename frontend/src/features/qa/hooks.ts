import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { generateQaReport, getQaReport } from './service'

export function useQaReport(projectId: string) {
  return useQuery({
    queryKey: ['qa', projectId],
    queryFn: () => getQaReport(projectId),
    retry: false,
  })
}

export function useGenerateQaReport(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => generateQaReport(projectId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['qa', projectId] })
    },
  })
}
