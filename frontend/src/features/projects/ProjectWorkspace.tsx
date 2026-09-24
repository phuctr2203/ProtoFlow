import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { MeetingsPage } from '@/features/meetings/MeetingsPage'

export function ProjectWorkspace() {
  const { projectId } = useParams<{ projectId: string }>()
  if (!projectId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <MeetingsPage projectId={projectId} />
    </WorkspaceShell>
  )
}
