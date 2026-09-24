import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { OverviewPage } from './OverviewPage'

export function OverviewRoute() {
  const { projectId } = useParams<{ projectId: string }>()
  if (!projectId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <OverviewPage projectId={projectId} />
    </WorkspaceShell>
  )
}
