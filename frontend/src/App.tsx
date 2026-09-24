import { WorkspaceShell } from '@/components/WorkspaceShell'
import { ProjectsPage } from '@/features/projects/ProjectsPage'

function App() {
  return (
    <WorkspaceShell>
      <ProjectsPage />
    </WorkspaceShell>
  )
}

export default App
