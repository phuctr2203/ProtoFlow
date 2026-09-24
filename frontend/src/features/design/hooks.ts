import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { generateDesign, getDesign } from './service'

export function useDesign(projectId: string) {
  return useQuery({
    queryKey: ['design', projectId],
    queryFn: () => getDesign(projectId),
    retry: false,
  })
}

export function useGenerateDesign(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => generateDesign(projectId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['design', projectId] })
    },
  })
}
