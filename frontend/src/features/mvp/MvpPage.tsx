import { Button } from '@/components/ui/button'
import type { Scope } from './types'
import { useGenerateMvp, useMvp } from './hooks'

const SCOPES: { key: Scope; label: string; color: string }[] = [
  { key: 'MUST_HAVE', label: 'Must have', color: 'text-red-700' },
  { key: 'SHOULD_HAVE', label: 'Should have', color: 'text-amber-700' },
  { key: 'NICE_TO_HAVE', label: 'Nice to have', color: 'text-slate-600' },
]

export function MvpPage({ projectId }: { projectId: string }) {
  const { data, isLoading, isError } = useMvp(projectId)
  const generate = useGenerateMvp(projectId)

  if (isLoading) return <p className="p-6 text-sm text-slate-500">Loading MVP…</p>

  if (isError || !data) {
    return (
      <div className="mx-auto max-w-3xl space-y-4 p-6">
        <h1 className="text-2xl font-semibold">MVP Specification</h1>
        <p className="text-sm text-slate-500">
          No MVP has been proposed yet. It is generated from the meeting intelligence.
        </p>
        <Button onClick={() => generate.mutate()} disabled={generate.isPending}>
          {generate.isPending ? 'Generating…' : 'Generate MVP'}
        </Button>
        {generate.isError && (
          <p className="text-sm text-red-600">Need processed meeting intelligence first.</p>
        )}
      </div>
    )
  }

  const spec = data.spec
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">MVP Specification</h1>
          <p className="text-sm text-slate-500">The smallest useful product to demo.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded bg-slate-100 px-2 py-1 font-mono text-xs text-slate-600">
            v{data.version}
          </span>
          <span className="rounded-full bg-green-50 px-2 py-1 text-xs font-semibold text-green-700">
            {data.status}
          </span>
        </div>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-400">Objective</h2>
        <p className="mt-1 text-sm text-slate-700">{spec.objective}</p>
        <p className="mt-2 text-sm text-slate-500">Users: {spec.target_users.join(', ')}</p>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Features
        </h2>
        {SCOPES.map(({ key, label, color }) => {
          const items = spec.features.filter((f) => f.scope === key)
          if (items.length === 0) return null
          return (
            <div key={key} className="mb-3">
              <div className={`text-xs font-bold ${color}`}>{label}</div>
              <ul className="mt-1 list-disc pl-5 text-sm text-slate-700">
                {items.map((f) => (
                  <li key={f.name}>{f.name}</li>
                ))}
              </ul>
            </div>
          )
        })}
        {spec.out_of_scope.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            <span className="text-xs font-bold text-slate-400">OUT OF SCOPE</span>
            {spec.out_of_scope.map((o) => (
              <span key={o} className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
                {o}
              </span>
            ))}
          </div>
        )}
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-400">
          Demo scenario
        </h2>
        <p className="mt-1 text-sm text-slate-700">{spec.demo_scenario}</p>
        {spec.acceptance_criteria.length > 0 && (
          <ul className="mt-3 list-disc pl-5 text-sm text-slate-600">
            {spec.acceptance_criteria.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
