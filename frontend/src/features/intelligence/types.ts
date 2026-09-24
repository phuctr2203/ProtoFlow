export interface Evidence {
  speaker?: string | null
  start_time?: number | null
  end_time?: number | null
  quote?: string | null
}

export interface Requirement {
  id: string
  description: string
  type: string
  priority: string
  extraction: 'EXPLICIT' | 'INFERRED'
  status: 'CONFIRMED' | 'NEEDS_REVIEW'
  source?: Evidence | null
  confidence: number
}

export interface MeetingIntelligence {
  business_context: {
    client?: string | null
    industry?: string | null
    problem: string
    goals: string[]
  }
  requirements: Requirement[]
  personas: { name: string; description: string }[]
  constraints: { description: string; kind: string }[]
  decisions: { description: string }[]
  risks: { description: string }[]
  open_questions: { question: string }[]
  action_items: { action: string; owner?: string | null; deadline?: string | null }[]
  validation_notes: string[]
}
