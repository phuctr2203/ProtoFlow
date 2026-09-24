export type ProjectStatus =
  | 'DISCOVERY'
  | 'MVP_DEFINITION'
  | 'DESIGN'
  | 'DEVELOPMENT'
  | 'QA'
  | 'DEMO_READY'
  | 'COMPLETED'

export interface Project {
  id: string
  name: string
  description: string | null
  status: ProjectStatus
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description?: string | null
}
