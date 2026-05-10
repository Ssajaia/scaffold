from abc import ABC, abstractmethod


class Runtime(ABC):
    @abstractmethod
    def detect_port(self) -> int:
        pass

    @abstractmethod
    def generate_dockerfile(self, port: int) -> str:
        pass

    def image_name(self, project_name: str) -> str:
        return f"scaffold-{project_name}"

    def container_name(self, project_name: str) -> str:
        return f"scaffold-{project_name}-container"
