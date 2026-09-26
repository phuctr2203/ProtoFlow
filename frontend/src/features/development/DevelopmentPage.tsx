import { Button } from '@/components/ui/button'
import { useCodeGeneration, useDevelopmentPlan, useGenerateCode } from './hooks'

export function DevelopmentPage({ projectId }: { projectId: string }) {
  const plan = useDevelopmentPlan(projectId)
  const code = useCodeGeneration(projectId)
  const generate = useGenerateCode(projectId)

  if (plan.isLoading) return <p className="p-6 text-sm text-slate-500">Loading development…</p>

  const hasPlan = !plan.isError && plan.data
  const result = !code.isError && code.data ? code.data : null

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Development</h1>
          <p className="text-sm text-slate-500">
            The Development Manager plans tasks and the coding engine implements them.
          </p>
        </div>
        <Button onClick={() => generate.mutate()} disabled={generate.isPending}>
          {generate.isPending ? 'Generating…' : 'Generate code'}
        </Button>
      </div>

      {generate.isError && (
        <p className="text-sm text-red-600">An approved MVP and a design are required first.</p>
      )}

      {!hasPlan && !result && (
        <p className="text-sm text-slate-500">
          No development plan yet. Generate code to break the MVP into tasks and implement them.
        </p>
      )}

      {hasPlan && (
        <section className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Task plan (MVP v{plan.data!.mvp_version})
          </h2>
          <ol className="space-y-2 text-sm">
            {plan.data!.plan.tasks.map((t) => (
              <li key={t.id} className="flex items-start gap-2">
                <span className="shrink-0 rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
                  {t.component}
                </span>
                <span className="text-slate-700">
                  <span className="font-medium">{t.id}</span> — {t.title}
                </span>
              </li>
            ))}
          </ol>
        </section>
      )}

      {result && (
        <section className="rounded-lg border border-slate-200 bg-white p-4">
          <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
            Generated code ({result.engine})
          </h2>
          <p className="mb-3 text-sm text-slate-700">{result.result.summary}</p>
          {result.result.pull_request_url && (
            <a
              href={result.result.pull_request_url}
              target="_blank"
              rel="noreferrer"
              className="text-sm font-medium text-indigo-700 hover:underline"
            >
              View pull request →
            </a>
          )}
          <div className="mt-3 flex flex-wrap gap-2">
            {result.result.files_changed.map((f) => (
              <span
                key={f}
                className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
              >
                {f}
              </span>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
