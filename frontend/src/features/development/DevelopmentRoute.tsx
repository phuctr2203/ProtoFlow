import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { DevelopmentPage } from './DevelopmentPage'

export function DevelopmentRoute() {
  const { projectId } = useParams<{ projectId: string }>()
  if (!projectId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <DevelopmentPage projectId={projectId} />
    </WorkspaceShell>
  )
}
