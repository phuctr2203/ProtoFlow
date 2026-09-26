import { api } from '@/lib/api'
import type { ProjectOverview } from './types'

export async function getOverview(projectId: string): Promise<ProjectOverview> {
  const { data } = await api.get<ProjectOverview>(`/projects/${projectId}/overview`)
  return data
}
