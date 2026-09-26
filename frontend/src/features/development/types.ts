export interface DevelopmentTask {
  id: string
  title: string
  description: string
  component: string
  depends_on: string[]
  order: number
}

export interface DevelopmentPlan {
  tasks: DevelopmentTask[]
}

export interface DevelopmentPlanResponse {
  mvp_version: number
  created_at: string
  plan: DevelopmentPlan
}

export interface CodingResult {
  summary: string
  files_changed: string[]
  tests_written: string[]
  branch: string | null
  pull_request_url: string | null
}

export interface CodeGenerationResponse {
  mvp_version: number
  created_at: string
  engine: string
  result: CodingResult
}
