import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { DemoPage } from './DemoPage'

export function DemoRoute() {
  const { projectId } = useParams<{ projectId: string }>()
  if (!projectId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <DemoPage projectId={projectId} />
    </WorkspaceShell>
  )
}
