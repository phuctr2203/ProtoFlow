import { api } from '@/lib/api'
import type { Meeting } from './types'

export async function listMeetings(projectId: string): Promise<Meeting[]> {
  const { data } = await api.get<Meeting[]>(`/projects/${projectId}/meetings`)
  return data
}

export async function simulateMeeting(projectId: string, fixture: string): Promise<void> {
  await api.post('/dev/simulate-meeting', { project_id: projectId, fixture })
}
