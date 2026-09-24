import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import {
  generateCode,
  generateDevelopmentPlan,
  getCodeGeneration,
  getDevelopmentPlan,
} from './service'

export function useDevelopmentPlan(projectId: string) {
  return useQuery({
    queryKey: ['development', projectId],
    queryFn: () => getDevelopmentPlan(projectId),
    retry: false,
  })
}

export function useCodeGeneration(projectId: string) {
  return useQuery({
    queryKey: ['code', projectId],
    queryFn: () => getCodeGeneration(projectId),
    retry: false,
  })
}

export function useGenerateDevelopmentPlan(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => generateDevelopmentPlan(projectId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['development', projectId] })
    },
  })
}

export function useGenerateCode(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => generateCode(projectId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ['development', projectId] })
      void queryClient.invalidateQueries({ queryKey: ['code', projectId] })
    },
  })
}
