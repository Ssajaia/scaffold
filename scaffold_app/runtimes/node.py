from pathlib import Path
from jinja2 import Template
from .base import Runtime

DOCKERFILE_TEMPLATE = """\
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE {{ port }}
CMD ["npm", "start"]
"""


class NodeRuntime(Runtime):
    def __init__(self, project_dir: Path, override_port: int | None = None):
        self._project_dir = project_dir
        self._override_port = override_port

    def detect_port(self) -> int:
        if self._override_port is not None:
            return self._override_port
        pkg = self._project_dir / "package.json"
        try:
            if "8080" in pkg.read_text():
                return 8080
        except OSError:
            pass
        return 3000

    def generate_dockerfile(self, port: int) -> str:
        return Template(DOCKERFILE_TEMPLATE).render(port=port)
