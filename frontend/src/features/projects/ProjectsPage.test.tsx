import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import type { ReactElement } from 'react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'

import { ProjectsPage } from './ProjectsPage'

vi.mock('./service', () => ({
  listProjects: vi.fn().mockResolvedValue([]),
  createProject: vi.fn(),
  getProject: vi.fn(),
}))

function renderWithClient(ui: ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>,
  )
}

describe('ProjectsPage', () => {
  it('renders the heading and the empty state', async () => {
    renderWithClient(<ProjectsPage />)
    expect(screen.getByRole('heading', { name: 'Projects' })).toBeInTheDocument()
    expect(await screen.findByText(/No projects yet/i)).toBeInTheDocument()
  })
})
