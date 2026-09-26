import { api } from '@/lib/api'
import type { DemoResponse } from './types'

export async function getDemo(projectId: string): Promise<DemoResponse> {
  const { data } = await api.get<DemoResponse>(`/projects/${projectId}/demo`)
  return data
}

export async function generateDemo(projectId: string): Promise<DemoResponse> {
  const { data } = await api.post<DemoResponse>(`/projects/${projectId}/demo`)
  return data
}
