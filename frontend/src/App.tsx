import { Route, Routes } from 'react-router-dom'

import { ProjectWorkspace } from '@/features/projects/ProjectWorkspace'
import { ProjectsPage } from '@/features/projects/ProjectsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<ProjectsPage />} />
      <Route path="/projects/:projectId/meetings" element={<ProjectWorkspace />} />
    </Routes>
  )
}

export default App
