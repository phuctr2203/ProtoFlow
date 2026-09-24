import { api } from '@/lib/api'
import type { DesignResponse } from './types'

export async function getDesign(projectId: string): Promise<DesignResponse> {
  const { data } = await api.get<DesignResponse>(`/projects/${projectId}/design`)
  return data
}

export async function generateDesign(projectId: string): Promise<DesignResponse> {
  const { data } = await api.post<DesignResponse>(`/projects/${projectId}/design`)
  return data
}
