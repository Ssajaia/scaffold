import shutil
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


def _check_docker_installed() -> tuple[bool, str]:
    path = shutil.which("docker")
    if path is None:
        return False, "not found in PATH"
    return True, path


def _check_docker_daemon() -> tuple[bool, str]:
    result = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        return False, "daemon not running"
    return True, "running"


def _check_project(project_dir: Path) -> tuple[bool, str]:
    has_node = (project_dir / "package.json").exists()
    has_python = (project_dir / "requirements.txt").exists()
    if has_node and has_python:
        return False, "ambiguous (both package.json and requirements.txt)"
    if has_node:
        return True, "node"
    if has_python:
        return True, "python"
    return False, "unsupported"


def run_doctor(project_dir: Path) -> None:
    table = Table(title="scaffold doctor", show_header=True, header_style="bold")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")

    all_ok = True

    docker_ok, docker_detail = _check_docker_installed()
    table.add_row("Docker installed", "[green]✓[/green]" if docker_ok else "[red]✗[/red]", docker_detail)
    if not docker_ok:
        all_ok = False

    if docker_ok:
        daemon_ok, daemon_detail = _check_docker_daemon()
        table.add_row("Docker daemon", "[green]✓[/green]" if daemon_ok else "[red]✗[/red]", daemon_detail)
        if not daemon_ok:
            all_ok = False
    else:
        table.add_row("Docker daemon", "[dim]skipped[/dim]", "docker not installed")

    project_ok, project_detail = _check_project(project_dir)
    table.add_row("Project supported", "[green]✓[/green]" if project_ok else "[red]✗[/red]", project_detail)
    if not project_ok:
        all_ok = False

    console.print(table)
    if not all_ok:
        sys.exit(1)
