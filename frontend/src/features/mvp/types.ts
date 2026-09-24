export type Scope = 'MUST_HAVE' | 'SHOULD_HAVE' | 'NICE_TO_HAVE' | 'OUT_OF_SCOPE'

export interface Feature {
  name: string
  description: string
  scope: Scope
}

export interface MVPSpecification {
  objective: string
  target_users: string[]
  goals: string[]
  features: Feature[]
  user_journeys: string[]
  acceptance_criteria: string[]
  out_of_scope: string[]
  assumptions: string[]
  open_questions: string[]
  demo_scenario: string
}

export interface MVPResponse {
  version: number
  status: string
  created_at: string
  spec: MVPSpecification
}
