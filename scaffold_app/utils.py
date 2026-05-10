import shutil
import subprocess
import sys
from rich.console import Console

console = Console()


def ensure_docker() -> None:
    if shutil.which("docker") is None:
        console.print("[red]Error:[/red] Docker is not installed or not in PATH.")
        sys.exit(1)
    result = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        console.print("[red]Error:[/red] Docker daemon is not running.")
        sys.exit(1)
