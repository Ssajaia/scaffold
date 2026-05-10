import subprocess
import sys
from rich.console import Console

console = Console()


def _run_cmd(cmd: list[str], verbose: bool) -> subprocess.CompletedProcess:
    if verbose:
        console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if verbose or result.returncode != 0:
        if result.stdout:
            console.print(result.stdout, end="")
    return result


def build(image_name: str, context_path: str, verbose: bool = False) -> None:
    result = _run_cmd(["docker", "build", "-t", image_name, context_path], verbose)
    if result.returncode != 0:
        console.print("[red]Docker build failed.[/red]")
        sys.exit(1)


def run(image_name: str, container_name: str, port: int, detach: bool = False, verbose: bool = False) -> None:
    cmd = ["docker", "run", "--name", container_name, "-p", f"{port}:{port}"]
    if detach:
        cmd.append("-d")
    cmd.append(image_name)
    result = _run_cmd(cmd, verbose)
    if result.returncode != 0:
        console.print("[red]Docker run failed.[/red]")
        sys.exit(1)
