"""Repository inspection (Story 6.2, Idea.MD §31 Rule 1). A deterministic scan of an existing
repository run before code generation, so the coding agents follow existing structure and
conventions rather than rewriting. No LLM required."""

from pathlib import Path

from app.ai.schemas.development import RepositoryInspection

_IGNORED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next"}

# Marker file -> framework/tech it implies.
_MARKERS: dict[str, str] = {
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "package.json": "Node.js",
    "vite.config.ts": "Vite",
    "vite.config.js": "Vite",
    "tsconfig.json": "TypeScript",
    "dockerfile": "Docker",
    "docker-compose.yml": "Docker Compose",
    "alembic.ini": "Alembic",
    "go.mod": "Go",
    "cargo.toml": "Rust",
}

_LANG_EXTS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".rb",
    ".sql",
    ".css",
}


def inspect_repository(root: str | Path) -> RepositoryInspection:
    root_path = Path(root)
    if not root_path.is_dir():
        return RepositoryInspection(notes=[f"Path {root_path} is not a directory"])

    languages: dict[str, int] = {}
    entry_points: list[str] = []
    frameworks: set[str] = set()
    file_count = 0

    for path in root_path.rglob("*"):
        if any(part in _IGNORED_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        file_count += 1

        marker = _MARKERS.get(path.name.lower())
        if marker:
            frameworks.add(marker)
            rel = str(path.relative_to(root_path))
            if rel not in entry_points:
                entry_points.append(rel)

        ext = path.suffix.lower()
        if ext in _LANG_EXTS:
            languages[ext] = languages.get(ext, 0) + 1

    top_level = sorted(p.name for p in root_path.iterdir() if p.name not in _IGNORED_DIRS)

    notes: list[str] = []
    if not frameworks:
        notes.append("No known framework markers found; treat as a greenfield repository.")

    return RepositoryInspection(
        file_count=file_count,
        languages=dict(sorted(languages.items(), key=lambda kv: kv[1], reverse=True)),
        frameworks=sorted(frameworks),
        entry_points=sorted(entry_points),
        top_level=top_level,
        notes=notes,
    )
