import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { createProject, listProjects } from './service'

const PROJECTS_KEY = ['projects'] as const

export function useProjects() {
  return useQuery({ queryKey: PROJECTS_KEY, queryFn: listProjects })
}

export function useCreateProject() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: createProject,
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: PROJECTS_KEY })
    },
  })
}
