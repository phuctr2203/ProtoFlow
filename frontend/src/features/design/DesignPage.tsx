import { Button } from '@/components/ui/button'
import { useDesign, useGenerateDesign } from './hooks'

function Chips({ items }: { items: string[] }) {
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((i) => (
        <span key={i} className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
          {i}
        </span>
      ))}
    </div>
  )
}

export function DesignPage({ projectId }: { projectId: string }) {
  const { data, isLoading, isError } = useDesign(projectId)
  const generate = useGenerateDesign(projectId)

  if (isLoading) return <p className="p-6 text-sm text-slate-500">Loading design…</p>

  if (isError || !data) {
    return (
      <div className="mx-auto max-w-3xl space-y-4 p-6">
        <h1 className="text-2xl font-semibold">MVP Design</h1>
        <p className="text-sm text-slate-500">
          No design yet. It is generated from the approved MVP.
        </p>
        <Button onClick={() => generate.mutate()} disabled={generate.isPending}>
          {generate.isPending ? 'Generating…' : 'Generate design'}
        </Button>
        {generate.isError && (
          <p className="text-sm text-red-600">An approved MVP is required first.</p>
        )}
      </div>
    )
  }

  const d = data.design
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold">MVP Design</h1>
        <p className="text-sm text-slate-500">
          Lightweight UX + technical design from MVP v{data.mvp_version}.
        </p>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          User journey
        </h2>
        <p className="text-sm text-slate-700">{d.user_journey.join('  →  ')}</p>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Screens
        </h2>
        <ul className="list-disc pl-5 text-sm text-slate-700">
          {d.screens.map((s) => (
            <li key={s.name}>
              <span className="font-medium">{s.name}</span> — {s.description}
            </li>
          ))}
        </ul>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Components
          </h2>
          <Chips items={d.components} />
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">APIs</h2>
          <Chips items={d.apis} />
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Data model
          </h2>
          <Chips items={d.data_model} />
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Tech decisions
          </h2>
          <ul className="list-disc pl-5 text-sm text-slate-700">
            {d.tech_decisions.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          AI workflow
        </h2>
        <ul className="list-disc pl-5 text-sm text-slate-700">
          {d.ai_workflow.map((w) => (
            <li key={w}>{w}</li>
          ))}
        </ul>
      </section>
    </div>
  )
}
