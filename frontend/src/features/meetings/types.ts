export type MeetingStatus =
  | 'SCHEDULED'
  | 'IN_PROGRESS'
  | 'COMPLETED'
  | 'TRANSCRIPT_PENDING'
  | 'TRANSCRIPT_READY'
  | 'PROCESSING'
  | 'PROCESSED'
  | 'FAILED'

export interface Meeting {
  id: string
  project_id: string
  provider: string
  external_meeting_id: string
  title: string
  status: MeetingStatus
  created_at: string
  updated_at: string
}

export const FIXTURES = [
  'clean',
  'asr_noisy',
  'diarization_noisy',
  'mixed_language',
  'combined',
] as const
