from pathlib import Path
from runpy import run_path


def test_docs_copy_only_active_notebooks(tmp_path):
    source = tmp_path / "notebooks"
    destination = tmp_path / "docs"
    source.mkdir()
    (source / "example.ipynb").write_text("{}", encoding="utf-8")
    (source / "credentials.json").write_text("{}", encoding="utf-8")
    (source / "config.json").write_text("{}", encoding="utf-8")
    (source / ".env").write_text("", encoding="utf-8")
    (source / "deprecated").mkdir()
    (source / "deprecated" / "old.ipynb").write_text("{}", encoding="utf-8")
    destination.mkdir()
    (destination / "README.md").write_text("Keep this file", encoding="utf-8")

    hook = run_path(
        str(Path(__file__).parents[1] / "docs" / "hooks" / "notebooks_json_output.py")
    )
    hook["_update_files_in_docs"](source, destination)

    assert {path.name for path in destination.iterdir()} == {
        "example.ipynb",
        "README.md",
    }
    assert (destination / "example.ipynb").read_text(encoding="utf-8") == "{}"
