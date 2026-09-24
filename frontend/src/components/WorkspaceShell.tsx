import type { ReactNode } from 'react'
import { Link, NavLink } from 'react-router-dom'

type Tab = { label: string; to: ((projectId: string) => string) | null }

const TABS: Tab[] = [
  { label: 'Overview', to: null },
  { label: 'Meetings', to: (id) => `/projects/${id}/meetings` },
  { label: 'Intelligence', to: null },
  { label: 'MVP', to: (id) => `/projects/${id}/mvp` },
  { label: 'Design', to: (id) => `/projects/${id}/design` },
  { label: 'Development', to: (id) => `/projects/${id}/development` },
  { label: 'QA', to: (id) => `/projects/${id}/qa` },
  { label: 'Demo', to: (id) => `/projects/${id}/demo` },
]

export function WorkspaceShell({
  projectId,
  children,
}: {
  projectId: string
  children: ReactNode
}) {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <aside className="w-56 shrink-0 border-r border-slate-200 bg-white p-4">
        <div className="mb-4 text-lg font-bold">ProtoFlow</div>
        <Link to="/" className="mb-4 block text-sm text-slate-500 hover:text-slate-800">
          ← All projects
        </Link>
        <nav className="space-y-1">
          {TABS.map((tab) =>
            tab.to ? (
              <NavLink
                key={tab.label}
                to={tab.to(projectId)}
                className={({ isActive }) =>
                  `block rounded-md px-3 py-2 text-sm ${
                    isActive
                      ? 'bg-indigo-50 font-semibold text-indigo-700'
                      : 'text-slate-600 hover:bg-slate-100'
                  }`
                }
              >
                {tab.label}
              </NavLink>
            ) : (
              <span
                key={tab.label}
                className="block cursor-not-allowed rounded-md px-3 py-2 text-sm text-slate-300"
                title="Coming in a later epic"
              >
                {tab.label}
              </span>
            ),
          )}
        </nav>
      </aside>
      <main className="flex-1">{children}</main>
    </div>
  )
}
