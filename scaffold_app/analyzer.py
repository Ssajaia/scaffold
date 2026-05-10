from dataclasses import dataclass
from pathlib import Path
from .runtimes.base import Runtime
from .runtimes.node import NodeRuntime
from .runtimes.python import PythonRuntime


@dataclass
class ProjectInfo:
    project_type: str
    runtime: Runtime
    project_name: str


def analyze(project_dir: Path, override_port: int | None = None) -> ProjectInfo:
    has_node = (project_dir / "package.json").exists()
    has_python = (project_dir / "requirements.txt").exists()

    if has_node and has_python:
        raise ValueError("Both package.json and requirements.txt found. Cannot determine project type.")
    if not has_node and not has_python:
        raise ValueError("No supported project files found. Expected package.json or requirements.txt.")

    project_name = project_dir.resolve().name.lower().replace(" ", "-")

    if has_node:
        return ProjectInfo("node", NodeRuntime(project_dir, override_port), project_name)

    return ProjectInfo("python", PythonRuntime(override_port), project_name)
