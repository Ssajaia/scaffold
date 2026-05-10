from jinja2 import Template
from .base import Runtime

DOCKERFILE_TEMPLATE = """\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE {{ port }}
CMD ["python", "main.py"]
"""


class PythonRuntime(Runtime):
    def __init__(self, override_port: int | None = None):
        self._override_port = override_port

    def detect_port(self) -> int:
        if self._override_port is not None:
            return self._override_port
        return 8000

    def generate_dockerfile(self, port: int) -> str:
        return Template(DOCKERFILE_TEMPLATE).render(port=port)
