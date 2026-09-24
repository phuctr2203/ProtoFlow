import { Button } from '@/components/ui/button'
import { useGenerateQaReport, useQaReport } from './hooks'
import type { TestStatus } from './types'

const STATUS_STYLES: Record<TestStatus, string> = {
  PASS: 'bg-green-100 text-green-700',
  FAIL: 'bg-red-100 text-red-700',
  BLOCKED: 'bg-amber-100 text-amber-700',
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 text-center">
      <div className="text-2xl font-semibold text-slate-900">{value}</div>
      <div className="text-xs uppercase tracking-wide text-slate-400">{label}</div>
    </div>
  )
}

export function QaPage({ projectId }: { projectId: string }) {
  const { data, isLoading, isError } = useQaReport(projectId)
  const generate = useGenerateQaReport(projectId)

  if (isLoading) return <p className="p-6 text-sm text-slate-500">Loading QA report…</p>

  if (isError || !data) {
    return (
      <div className="mx-auto max-w-3xl space-y-4 p-6">
        <h1 className="text-2xl font-semibold">Automated QA</h1>
        <p className="text-sm text-slate-500">
          No QA report yet. It is generated from the MVP after code generation.
        </p>
        <Button onClick={() => generate.mutate()} disabled={generate.isPending}>
          {generate.isPending ? 'Running QA…' : 'Run QA'}
        </Button>
        {generate.isError && (
          <p className="text-sm text-red-600">
            An approved MVP and generated code are required first.
          </p>
        )}
      </div>
    )
  }

  const r = data.report
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Automated QA</h1>
          <p className="text-sm text-slate-500">Coverage &amp; results for MVP v{data.mvp_version}.</p>
        </div>
        <span
          className={`rounded-full px-3 py-1 text-sm font-semibold ${
            data.demo_ready ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
          }`}
        >
          {data.demo_ready ? 'Demo-ready' : 'Not demo-ready'}
        </span>
      </div>

      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <Stat label="Total" value={r.total} />
        <Stat label="Passed" value={r.passed} />
        <Stat label="Failed" value={r.failed} />
        <Stat label="Blocked" value={r.blocked} />
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Requirement coverage
        </h2>
        <ul className="space-y-2 text-sm">
          {r.coverage.map((c) => (
            <li key={c.feature} className="flex items-center justify-between gap-2">
              <span className="text-slate-700">
                {c.feature}{' '}
                <span className="text-xs text-slate-400">({c.scope})</span>
              </span>
              <span className={c.covered ? 'text-green-600' : 'text-red-600'}>
                {c.covered ? `✓ ${c.test_ids.length} test(s)` : '✗ uncovered'}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Test cases
        </h2>
        <ul className="space-y-2 text-sm">
          {r.test_cases.map((t) => (
            <li key={t.id} className="flex items-start justify-between gap-3">
              <span className="text-slate-700">
                <span className="font-medium">{t.id}</span> — {t.title}
                {t.failure_reason && (
                  <span className="block text-xs text-red-600">{t.failure_reason}</span>
                )}
              </span>
              <span
                className={`shrink-0 rounded px-2 py-0.5 text-xs font-semibold ${
                  STATUS_STYLES[t.status]
                }`}
              >
                {t.status}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <Button
        variant="outline"
        onClick={() => generate.mutate()}
        disabled={generate.isPending}
      >
        {generate.isPending ? 'Re-running QA…' : 'Re-run QA'}
      </Button>
    </div>
  )
}
