import { Route, Routes } from 'react-router-dom'

import { DesignRoute } from '@/features/design/DesignRoute'
import { IntelligenceRoute } from '@/features/intelligence/IntelligenceRoute'
import { MvpRoute } from '@/features/mvp/MvpRoute'
import { ProjectWorkspace } from '@/features/projects/ProjectWorkspace'
import { ProjectsPage } from '@/features/projects/ProjectsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<ProjectsPage />} />
      <Route path="/projects/:projectId/meetings" element={<ProjectWorkspace />} />
      <Route
        path="/projects/:projectId/meetings/:meetingId/intelligence"
        element={<IntelligenceRoute />}
      />
      <Route path="/projects/:projectId/mvp" element={<MvpRoute />} />
      <Route path="/projects/:projectId/design" element={<DesignRoute />} />
    </Routes>
  )
}

export default App
