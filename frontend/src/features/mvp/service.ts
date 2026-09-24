import { api } from '@/lib/api'
import type { MVPResponse } from './types'

export async function getMvp(projectId: string): Promise<MVPResponse> {
  const { data } = await api.get<MVPResponse>(`/projects/${projectId}/mvp`)
  return data
}

export async function generateMvp(projectId: string): Promise<MVPResponse> {
  const { data } = await api.post<MVPResponse>(`/projects/${projectId}/mvp`)
  return data
}
