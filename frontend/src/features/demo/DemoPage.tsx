import { Button } from '@/components/ui/button'
import { useDemo, useGenerateDemo } from './hooks'
import type { CapabilityStatus } from './types'

const STATUS_STYLES: Record<CapabilityStatus, string> = {
  IMPLEMENTED: 'bg-green-100 text-green-700',
  SIMULATED: 'bg-amber-100 text-amber-700',
  NOT_IMPLEMENTED: 'bg-slate-100 text-slate-500',
}

function List({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4">
      <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">{title}</h2>
      <ul className="list-disc pl-5 text-sm text-slate-700">
        {items.map((i) => (
          <li key={i}>{i}</li>
        ))}
      </ul>
    </section>
  )
}

export function DemoPage({ projectId }: { projectId: string }) {
  const { data, isLoading, isError } = useDemo(projectId)
  const generate = useGenerateDemo(projectId)

  if (isLoading) return <p className="p-6 text-sm text-slate-500">Loading demo…</p>

  if (isError || !data) {
    return (
      <div className="mx-auto max-w-3xl space-y-4 p-6">
        <h1 className="text-2xl font-semibold">Demo</h1>
        <p className="text-sm text-slate-500">
          No demo prepared yet. It is generated from the MVP after QA.
        </p>
        <Button onClick={() => generate.mutate()} disabled={generate.isPending}>
          {generate.isPending ? 'Preparing…' : 'Prepare demo'}
        </Button>
        {generate.isError && (
          <p className="text-sm text-red-600">An approved MVP and a QA report are required first.</p>
        )}
      </div>
    )
  }

  const d = data.demo
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Demo</h1>
          <p className="text-sm text-slate-500">Package for MVP v{data.mvp_version}.</p>
        </div>
        <Button onClick={() => alert('Demo launch is a later capability.')}>Start demo</Button>
      </div>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Objective
        </h2>
        <p className="text-sm text-slate-700">{d.objective}</p>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">Script</h2>
        <ol className="space-y-2 text-sm text-slate-700">
          {d.script.map((s) => (
            <li key={s.order} className="flex gap-2">
              <span className="font-medium">{s.order}.</span>
              <span>
                {s.action}
                {s.expected && <span className="text-slate-400"> → {s.expected}</span>}
              </span>
            </li>
          ))}
        </ol>
      </section>

      <section className="rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Capabilities (honest labeling)
        </h2>
        <ul className="space-y-2 text-sm">
          {d.capabilities.map((c) => (
            <li key={c.name} className="flex items-center justify-between gap-2">
              <span className="text-slate-700">{c.name}</span>
              <span
                className={`shrink-0 rounded px-2 py-0.5 text-xs font-semibold ${
                  STATUS_STYLES[c.status]
                }`}
              >
                {c.status}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <List title="Synthetic data" items={d.synthetic_data} />
      <List title="Known limitations" items={d.known_limitations} />
      <List title="Next steps" items={d.next_steps} />
    </div>
  )
}
