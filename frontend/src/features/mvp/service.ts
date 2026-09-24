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

export type ApprovalAction = 'APPROVE' | 'REJECT' | 'REQUEST_REVISION'

export async function decideMvp(
  projectId: string,
  version: number,
  action: ApprovalAction,
): Promise<void> {
  await api.post(`/projects/${projectId}/mvp/approve`, {
    version,
    action,
    approved_by: 'consultant',
  })
}
