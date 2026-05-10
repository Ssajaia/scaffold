import tempfile
import shutil
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console

from .analyzer import analyze
from .doctor import run_doctor
from .docker_engine import build, run as docker_run
from .utils import ensure_docker

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def up(
    port: Optional[int] = typer.Option(None, "--port", help="Port to expose"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run container in background"),
    project_dir: Optional[Path] = typer.Option(None, "--project-dir"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    cwd = project_dir or Path.cwd()

    ensure_docker()

    try:
        info = analyze(cwd, override_port=port)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    resolved_port = info.runtime.detect_port()
    image = info.runtime.image_name(info.project_name)
    container = info.runtime.container_name(info.project_name)

    console.print(f"[bold]Project:[/bold] {info.project_name} ({info.project_type})")
    console.print(f"[bold]Port:[/bold] {resolved_port}")
    console.print(f"[bold]Image:[/bold] {image}")

    with tempfile.TemporaryDirectory() as tmpdir:
        dockerfile_content = info.runtime.generate_dockerfile(resolved_port)
        (Path(tmpdir) / "Dockerfile").write_text(dockerfile_content)

        for item in cwd.iterdir():
            dest = Path(tmpdir) / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        console.print("[bold]Building image...[/bold]")
        build(image, tmpdir, verbose=verbose)

    console.print("[bold]Starting container...[/bold]")
    docker_run(image, container, resolved_port, detach=detach, verbose=verbose)

    console.print(f"\n[green]Application running at:[/green] http://localhost:{resolved_port}")


@app.command()
def doctor(
    project_dir: Optional[Path] = typer.Option(None, "--project-dir"),
):
    cwd = project_dir or Path.cwd()
    run_doctor(cwd)
