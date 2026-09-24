import { Route, Routes } from 'react-router-dom'

import { DemoRoute } from '@/features/demo/DemoRoute'
import { DesignRoute } from '@/features/design/DesignRoute'
import { DevelopmentRoute } from '@/features/development/DevelopmentRoute'
import { IntelligenceRoute } from '@/features/intelligence/IntelligenceRoute'
import { MvpRoute } from '@/features/mvp/MvpRoute'
import { ProjectWorkspace } from '@/features/projects/ProjectWorkspace'
import { ProjectsPage } from '@/features/projects/ProjectsPage'
import { QaRoute } from '@/features/qa/QaRoute'

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
      <Route path="/projects/:projectId/development" element={<DevelopmentRoute />} />
      <Route path="/projects/:projectId/qa" element={<QaRoute />} />
      <Route path="/projects/:projectId/demo" element={<DemoRoute />} />
    </Routes>
  )
}

export default App
