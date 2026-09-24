import { useState } from 'react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import type { MeetingStatus } from './types'
import { FIXTURES } from './types'
import { useMeetings, useSimulateMeeting } from './hooks'

const STATUS_STYLE: Record<string, { color: string; bg: string }> = {
  TRANSCRIPT_READY: { color: '#027A48', bg: '#ECFDF3' },
  PROCESSED: { color: '#027A48', bg: '#ECFDF3' },
  PROCESSING: { color: '#B54708', bg: '#FFFAEB' },
  TRANSCRIPT_PENDING: { color: '#B54708', bg: '#FFFAEB' },
  FAILED: { color: '#B42318', bg: '#FEF3F2' },
}

function StatusBadge({ status }: { status: MeetingStatus }) {
  const s = STATUS_STYLE[status] ?? { color: '#475467', bg: '#F2F4F7' }
  return (
    <span
      style={{
        fontSize: 11,
        fontWeight: 600,
        color: s.color,
        background: s.bg,
        padding: '3px 8px',
        borderRadius: 999,
      }}
    >
      {status}
    </span>
  )
}

export function MeetingsPage({ projectId }: { projectId: string }) {
  const { data: meetings, isLoading, isError } = useMeetings(projectId)
  const simulate = useSimulateMeeting(projectId)
  const [fixture, setFixture] = useState<string>(FIXTURES[0])

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Meetings</h1>
          <p className="text-sm text-slate-500">
            A completed meeting's transcript is processed automatically. v1 simulates meetings with
            mock transcripts.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={fixture}
            onChange={(e) => setFixture(e.target.value)}
            aria-label="Transcript fixture"
            className="h-9 rounded-md border border-slate-300 px-2 text-sm"
          >
            {FIXTURES.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>
          <Button onClick={() => simulate.mutate(fixture)} disabled={simulate.isPending}>
            {simulate.isPending ? 'Simulating…' : 'Simulate meeting'}
          </Button>
        </div>
      </div>

      {isLoading && <p className="text-sm text-slate-500">Loading meetings…</p>}
      {isError && <p className="text-sm text-red-600">Could not load meetings.</p>}
      {meetings && meetings.length === 0 && (
        <p className="text-sm text-slate-500">
          No meetings yet. Simulate one to run it through the pipeline.
        </p>
      )}

      {meetings && meetings.length > 0 && (
        <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-slate-50 text-left text-slate-500">
                <th className="px-4 py-2 font-semibold">Meeting</th>
                <th className="px-4 py-2 font-semibold">Provider</th>
                <th className="px-4 py-2 font-semibold">Status</th>
                <th className="px-4 py-2 font-semibold">Intelligence</th>
              </tr>
            </thead>
            <tbody>
              {meetings.map((m) => (
                <tr key={m.id} className="border-t border-slate-100">
                  <td className="px-4 py-3 font-medium">{m.title}</td>
                  <td className="px-4 py-3 text-slate-500">{m.provider}</td>
                  <td className="px-4 py-3">
                    <StatusBadge status={m.status} />
                  </td>
                  <td className="px-4 py-3">
                    <Link
                      to={`/projects/${projectId}/meetings/${m.id}/intelligence`}
                      className="text-sm font-semibold text-indigo-600 hover:text-indigo-800"
                    >
                      View →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
