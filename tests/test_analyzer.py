import pytest
from pathlib import Path
from scaffold_app.analyzer import analyze


def test_node_detection(tmp_path):
    (tmp_path / "package.json").write_text('{"scripts": {"start": "node index.js"}}')
    assert analyze(tmp_path).project_type == "node"


def test_python_detection(tmp_path):
    (tmp_path / "requirements.txt").write_text("flask\n")
    assert analyze(tmp_path).project_type == "python"


def test_ambiguous_raises(tmp_path):
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "requirements.txt").write_text("")
    with pytest.raises(ValueError):
        analyze(tmp_path)


def test_unsupported_raises(tmp_path):
    with pytest.raises(ValueError):
        analyze(tmp_path)


def test_node_port_default(tmp_path):
    (tmp_path / "package.json").write_text('{"scripts": {"start": "node index.js"}}')
    assert analyze(tmp_path).runtime.detect_port() == 3000


def test_node_port_8080(tmp_path):
    (tmp_path / "package.json").write_text('{"port": "8080"}')
    assert analyze(tmp_path).runtime.detect_port() == 8080


def test_override_port(tmp_path):
    (tmp_path / "package.json").write_text("{}")
    assert analyze(tmp_path, override_port=5000).runtime.detect_port() == 5000


def test_python_port_default(tmp_path):
    (tmp_path / "requirements.txt").write_text("")
    assert analyze(tmp_path).runtime.detect_port() == 8000
