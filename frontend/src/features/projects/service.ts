import { api } from '@/lib/api'
import type { Project, ProjectCreate } from './types'

export async function listProjects(): Promise<Project[]> {
  const { data } = await api.get<Project[]>('/projects')
  return data
}

export async function createProject(payload: ProjectCreate): Promise<Project> {
  const { data } = await api.post<Project>('/projects', payload)
  return data
}

export async function getProject(id: string): Promise<Project> {
  const { data } = await api.get<Project>(`/projects/${id}`)
  return data
}
