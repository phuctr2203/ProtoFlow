import { api } from '@/lib/api'
import type { MeetingIntelligence } from './types'

export async function getIntelligence(meetingId: string): Promise<MeetingIntelligence> {
  const { data } = await api.get<MeetingIntelligence>(`/meetings/${meetingId}/intelligence`)
  return data
}
