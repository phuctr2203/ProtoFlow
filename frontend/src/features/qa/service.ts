import { api } from '@/lib/api'
import type { QAReportResponse } from './types'

export async function getQaReport(projectId: string): Promise<QAReportResponse> {
  const { data } = await api.get<QAReportResponse>(`/projects/${projectId}/qa`)
  return data
}

export async function generateQaReport(projectId: string): Promise<QAReportResponse> {
  const { data } = await api.post<QAReportResponse>(`/projects/${projectId}/qa`)
  return data
}
