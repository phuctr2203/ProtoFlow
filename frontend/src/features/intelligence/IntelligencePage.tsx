import type { Requirement } from './types'
import { useIntelligence } from './hooks'

function StatusBadge({ status }: { status: Requirement['status'] }) {
  const confirmed = status === 'CONFIRMED'
  return (
    <span
      className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
        confirmed ? 'bg-green-50 text-green-700' : 'bg-amber-50 text-amber-700'
      }`}
    >
      {status}
    </span>
  )
}

export function IntelligencePage({ meetingId }: { meetingId: string }) {
  const { data, isLoading, isError } = useIntelligence(meetingId)

  if (isLoading) return <p className="p-6 text-sm text-slate-500">Loading intelligence…</p>
  if (isError || !data)
    return (
      <p className="p-6 text-sm text-slate-500">
        Intelligence is not available yet. It is generated automatically after a transcript is
        processed.
      </p>
    )

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold">Meeting Intelligence</h1>
        <p className="text-sm text-slate-500">
          Every requirement links to the evidence that supports it — or is flagged for review.
        </p>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-400">Problem</h2>
        <p className="mt-1 text-sm text-slate-700">{data.business_context.problem}</p>
        {data.business_context.goals.length > 0 && (
          <ul className="mt-3 list-disc pl-5 text-sm text-slate-600">
            {data.business_context.goals.map((g) => (
              <li key={g}>{g}</li>
            ))}
          </ul>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-slate-400">
          Requirements
        </h2>
        {data.requirements.map((req) => (
          <div key={req.id} className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="mb-2 flex flex-wrap items-center gap-2">
              <span className="rounded bg-indigo-50 px-2 py-0.5 font-mono text-xs text-indigo-700">
                {req.id}
              </span>
              <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                {req.priority}
              </span>
              <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                {req.extraction}
              </span>
              <StatusBadge status={req.status} />
              <span className="ml-auto text-xs text-slate-500">
                Confidence {Math.round(req.confidence * 100)}%
              </span>
            </div>
            <p className="text-sm font-medium text-slate-800">{req.description}</p>
            {req.source?.quote ? (
              <div className="mt-2 rounded-md border border-slate-100 bg-slate-50 p-2">
                <p className="text-sm italic text-slate-600">“{req.source.quote}”</p>
                <p className="mt-1 font-mono text-xs text-slate-400">
                  {req.source.speaker ?? 'Unknown'}
                  {req.source.start_time != null ? ` · ${req.source.start_time}s` : ''}
                </p>
              </div>
            ) : (
              <p className="mt-2 font-mono text-xs text-slate-400">
                No direct quote — inferred, not client-confirmed scope.
              </p>
            )}
          </div>
        ))}
      </section>
    </div>
  )
}
