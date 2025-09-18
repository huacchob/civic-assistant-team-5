"""Test langsmith."""

import os

import pytest

from tests.conftest import load_environment_variables

load_environment_variables()
os.environ["OPENAI_API_KEY"] = os.getenv(key="OPENAI_API_KEY")

# Force LangSmith tracing (in case not loaded from .env)
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_PROJECT"] = os.getenv(
    "LANGSMITH_PROJECT", "civic-assistant-team-5"
)


def test_langsmith_connection(langsmith_client):
    """Test case for langsmith integration."""
    try:
        projects = list(langsmith_client.list_projects())
        assert projects is not None, (
            "No projects returned. Connection might not be established."
        )
        for project in projects:
            if project.name == "civic-assistant-team-5":
                print(f"Found project: {project.name} with ID: {project.id}")
                break
        else:
            pytest.fail("Project 'civic-assistant-team-5' not found.")
    except Exception as e:
        pytest.fail(f"Failed to connect to LangSmith: {e}")
