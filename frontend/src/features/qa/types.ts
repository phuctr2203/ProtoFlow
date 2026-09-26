export type TestStatus = 'PASS' | 'FAIL' | 'BLOCKED'

export interface TestCase {
  id: string
  feature: string
  title: string
  steps: string[]
  expected: string
  status: TestStatus
  evidence: string
  failure_reason: string | null
}

export interface FeatureCoverage {
  feature: string
  scope: string
  covered: boolean
  test_ids: string[]
}

export interface QAReport {
  test_cases: TestCase[]
  coverage: FeatureCoverage[]
  total: number
  passed: number
  failed: number
  blocked: number
  must_have_covered: boolean
  demo_ready: boolean
}

export interface QAReportResponse {
  mvp_version: number
  created_at: string
  demo_ready: boolean
  report: QAReport
}
