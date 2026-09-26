export interface PhaseStatus {
  phase: string
  status: 'complete' | 'pending' | 'awaiting_approval'
  detail: string
}

export interface ProjectOverview {
  project_id: string
  phases: PhaseStatus[]
}
