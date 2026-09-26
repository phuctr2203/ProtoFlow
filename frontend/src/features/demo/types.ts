export type CapabilityStatus = 'IMPLEMENTED' | 'SIMULATED' | 'NOT_IMPLEMENTED'

export interface DemoStep {
  order: number
  action: string
  expected: string
}

export interface Capability {
  name: string
  status: CapabilityStatus
  note: string
}

export interface DemoPackage {
  objective: string
  script: DemoStep[]
  synthetic_data: string[]
  known_limitations: string[]
  next_steps: string[]
  capabilities: Capability[]
}

export interface DemoResponse {
  mvp_version: number
  created_at: string
  demo: DemoPackage
}
