import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { IntelligencePage } from './IntelligencePage'

export function IntelligenceRoute() {
  const { projectId, meetingId } = useParams<{ projectId: string; meetingId: string }>()
  if (!projectId || !meetingId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <IntelligencePage meetingId={meetingId} />
    </WorkspaceShell>
  )
}
