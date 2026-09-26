import { useOverview } from './hooks'
import type { PhaseStatus } from './types'

const STATUS_STYLES: Record<PhaseStatus['status'], string> = {
  complete: 'bg-green-100 text-green-700',
  awaiting_approval: 'bg-amber-100 text-amber-700',
  pending: 'bg-slate-100 text-slate-400',
}

const STATUS_LABEL: Record<PhaseStatus['status'], string> = {
  complete: 'Complete',
  awaiting_approval: 'Awaiting approval',
  pending: 'Pending',
}

export function OverviewPage({ projectId }: { projectId: string }) {
  const { data, isLoading, isError } = useOverview(projectId)

  if (isLoading) return <p className="p-6 text-sm text-slate-500">Loading overview…</p>
  if (isError || !data) return <p className="p-6 text-sm text-red-600">Could not load overview.</p>

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold">Overview</h1>
        <p className="text-sm text-slate-500">Status across every phase of this engagement.</p>
      </div>

      <ol className="space-y-2">
        {data.phases.map((p, i) => (
          <li
            key={p.phase}
            className="flex items-center justify-between rounded-lg border border-slate-200 bg-white p-4"
          >
            <span className="flex items-center gap-3">
              <span className="text-xs font-medium text-slate-400">{i + 1}</span>
              <span className="font-medium text-slate-800">{p.phase}</span>
              {p.detail && <span className="text-xs text-slate-400">{p.detail}</span>}
            </span>
            <span
              className={`rounded-full px-3 py-1 text-xs font-semibold ${STATUS_STYLES[p.status]}`}
            >
              {STATUS_LABEL[p.status]}
            </span>
          </li>
        ))}
      </ol>
    </div>
  )
}
