import { type FormEvent, useState } from 'react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useCreateProject, useProjects } from './hooks'

export function ProjectsPage() {
  const { data: projects, isLoading, isError } = useProjects()
  const createProject = useCreateProject()
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!name.trim()) return
    createProject.mutate(
      { name: name.trim(), description: description.trim() || null },
      {
        onSuccess: () => {
          setName('')
          setDescription('')
        },
      },
    )
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold">Projects</h1>
        <p className="text-sm text-slate-500">Create a project to start a client engagement.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>New project</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-3">
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              placeholder="Project name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              aria-label="Project name"
            />
            <textarea
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              aria-label="Project description"
            />
            <Button type="submit" disabled={createProject.isPending || !name.trim()}>
              {createProject.isPending ? 'Creating…' : 'Create project'}
            </Button>
            {createProject.isError && (
              <p className="text-sm text-red-600">Could not create the project. Try again.</p>
            )}
          </form>
        </CardContent>
      </Card>

      <div className="space-y-3">
        {isLoading && <p className="text-sm text-slate-500">Loading projects…</p>}
        {isError && (
          <p className="text-sm text-red-600">Could not load projects. Is the backend running?</p>
        )}
        {projects && projects.length === 0 && (
          <p className="text-sm text-slate-500">No projects yet. Create your first one above.</p>
        )}
        {projects?.map((project) => (
          <Link key={project.id} to={`/projects/${project.id}/meetings`} className="block">
            <Card className="transition-colors hover:border-indigo-400">
              <CardHeader>
                <CardTitle>{project.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600">{project.description ?? 'No description'}</p>
                <span className="mt-2 inline-block rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-700">
                  {project.status}
                </span>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
