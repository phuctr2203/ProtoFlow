from pathlib import Path

from app.domain.development.inspection import inspect_repository


def test_inspect_detects_frameworks_and_languages(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    (tmp_path / "app").mkdir()
    (tmp_path / "app" / "main.py").write_text("print('hi')\n")
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend" / "package.json").write_text("{}\n")
    (tmp_path / "frontend" / "index.tsx").write_text("export {}\n")
    # Ignored dirs must not be counted.
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "HEAD").write_text("ref: refs/heads/main\n")

    result = inspect_repository(tmp_path)

    assert "Python" in result.frameworks
    assert "Node.js" in result.frameworks
    assert result.languages.get(".py") == 1
    assert result.languages.get(".tsx") == 1
    assert "pyproject.toml" in result.entry_points
    assert "app" in result.top_level and "frontend" in result.top_level
    assert ".git" not in result.top_level
    # .git/HEAD is ignored, so only the 4 real files are counted.
    assert result.file_count == 4


def test_inspect_greenfield_repo_notes_it(tmp_path: Path):
    (tmp_path / "README.md").write_text("# empty\n")
    result = inspect_repository(tmp_path)
    assert result.frameworks == []
    assert any("greenfield" in n for n in result.notes)


def test_inspect_non_directory_is_safe(tmp_path: Path):
    missing = tmp_path / "nope"
    result = inspect_repository(missing)
    assert result.file_count == 0
    assert result.notes
