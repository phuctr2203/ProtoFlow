import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { generateDemo, getDemo } from './service'

export function useDemo(projectId: string) {
  return useQuery({
    queryKey: ['demo', projectId],
    queryFn: () => getDemo(projectId),
    retry: false,
  })
}

export function useGenerateDemo(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => generateDemo(projectId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['demo', projectId] })
    },
  })
}
