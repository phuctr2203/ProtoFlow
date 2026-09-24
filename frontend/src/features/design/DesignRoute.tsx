import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { DesignPage } from './DesignPage'

export function DesignRoute() {
  const { projectId } = useParams<{ projectId: string }>()
  if (!projectId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <DesignPage projectId={projectId} />
    </WorkspaceShell>
  )
}
