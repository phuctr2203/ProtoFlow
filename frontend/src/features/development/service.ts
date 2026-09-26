import { api } from '@/lib/api'
import type { CodeGenerationResponse, DevelopmentPlanResponse } from './types'

export async function getDevelopmentPlan(projectId: string): Promise<DevelopmentPlanResponse> {
  const { data } = await api.get<DevelopmentPlanResponse>(`/projects/${projectId}/development`)
  return data
}

export async function generateDevelopmentPlan(
  projectId: string,
): Promise<DevelopmentPlanResponse> {
  const { data } = await api.post<DevelopmentPlanResponse>(`/projects/${projectId}/development`)
  return data
}

export async function getCodeGeneration(projectId: string): Promise<CodeGenerationResponse> {
  const { data } = await api.get<CodeGenerationResponse>(`/projects/${projectId}/code`)
  return data
}

export async function generateCode(projectId: string): Promise<CodeGenerationResponse> {
  const { data } = await api.post<CodeGenerationResponse>(`/projects/${projectId}/code`)
  return data
}
