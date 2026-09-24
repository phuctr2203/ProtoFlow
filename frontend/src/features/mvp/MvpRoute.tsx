import { useParams } from 'react-router-dom'

import { WorkspaceShell } from '@/components/WorkspaceShell'
import { MvpPage } from './MvpPage'

export function MvpRoute() {
  const { projectId } = useParams<{ projectId: string }>()
  if (!projectId) return null
  return (
    <WorkspaceShell projectId={projectId}>
      <MvpPage projectId={projectId} />
    </WorkspaceShell>
  )
}
