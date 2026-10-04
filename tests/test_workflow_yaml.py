"""
Tests for GitHub Actions workflow YAML validation.
"""
import pytest
import yaml
from pathlib import Path


def test_eval_workflow_yaml_exists():
    """ .github/workflows/eval.yml exists """
    workflow_path = Path(".github/workflows/eval.yml")
    assert workflow_path.exists(), "eval.yml should exist"


def test_eval_workflow_yaml_valid_yaml():
    """ eval.yml parses as valid YAML """
    workflow_path = Path(".github/workflows/eval.yml")
    with open(workflow_path, "r") as f:
        data = yaml.safe_load(f)
    assert data is not None


def test_eval_workflow_yaml_has_required_keys():
    """ eval.yml has 'on' (or True from YAML parsing), 'jobs', and 'permissions' keys """
    workflow_path = Path(".github/workflows/eval.yml")
    with open(workflow_path, "r") as f:
        data = yaml.safe_load(f)
    # PyYAML interprets bare 'on' key as boolean True
    assert "on" in data or True in data, "Workflow should have 'on' key (or True from YAML parsing)"
    assert "jobs" in data, "Workflow should have 'jobs' key"
    assert "permissions" in data, "Workflow should have 'permissions' key"


def test_eval_job_exists_with_ubuntu():
    """ Job 'eval' exists with runs-on ubuntu-latest """
    workflow_path = Path(".github/workflows/eval.yml")
    with open(workflow_path, "r") as f:
        data = yaml.safe_load(f)
    assert "eval" in data.get("jobs", {}), "Job 'eval' should exist"
    job = data["jobs"]["eval"]
    assert job.get("runs-on") == "ubuntu-latest", "Job should run on ubuntu-latest"


def test_groq_api_key_referenced():
    """ GROQ_API_KEY is referenced in the workflow """
    workflow_path = Path(".github/workflows/eval.yml")
    with open(workflow_path, "r") as f:
        content = f.read()
    assert "GROQ_API_KEY" in content, "GROQ_API_KEY should be referenced"


def test_workflow_uses_pull_request():
    """ Workflow uses pull_request (not pull_request_target )"""
    workflow_path = Path(".github/workflows/eval.yml")
    with open(workflow_path, "r") as f:
        content = f.read()
    assert "pull_request" in content, "Workflow should use pull_request"
    assert "pull_request_target" not in content, "Workflow should not use pull_request_target"