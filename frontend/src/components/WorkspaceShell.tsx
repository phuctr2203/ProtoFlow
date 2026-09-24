import type { ReactNode } from 'react'

const NAV_ITEMS = [
  'Overview',
  'Meetings',
  'Intelligence',
  'MVP',
  'Design',
  'Development',
  'QA',
  'Demo',
] as const

export function WorkspaceShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <aside className="w-56 shrink-0 border-r border-slate-200 bg-white p-4">
        <div className="mb-6 text-lg font-bold">ProtoFlow</div>
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => (
            <button
              key={item}
              type="button"
              className="block w-full rounded-md px-3 py-2 text-left text-sm text-slate-600 hover:bg-slate-100"
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>
      <main className="flex-1">{children}</main>
    </div>
  )
}
