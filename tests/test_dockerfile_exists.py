"""
Tests for Dockerfile validation.
"""
import pytest
from pathlib import Path


def test_dockerfile_exists_at_repo_root():
    """ Dockerfile exists at repo root """
    dockerfile_path = Path("Dockerfile")
    assert dockerfile_path.exists(), "Dockerfile should exist at repo root"


def test_dockerfile_contains_python_slim():
    """ Dockerfile contains 'FROM python:3.11-slim' """
    dockerfile_path = Path("Dockerfile")
    with open(dockerfile_path, "r") as f:
        content = f.read()
    assert "FROM python:3.11-slim" in content, "Dockerfile should contain FROM python:3.11-slim"


def test_dockerfile_contains_entrypoint():
    """ Dockerfile contains 'ENTRYPOINT' """
    dockerfile_path = Path("Dockerfile")
    with open(dockerfile_path, "r") as f:
        content = f.read()
    assert "ENTRYPOINT" in content, "Dockerfile should contain ENTRYPOINT"


def test_dockerfile_contains_evaluate_py():
    """ Dockerfile contains 'scripts/evaluate.py' """
    dockerfile_path = Path("Dockerfile")
    with open(dockerfile_path, "r") as f:
        content = f.read()
    assert "scripts/evaluate.py" in content, "Dockerfile should contain scripts/evaluate.py"