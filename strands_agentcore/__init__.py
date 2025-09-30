# strands_agentcore/__init__.py
__version__ = "0.1.0"

# re-export main small helpers for tests
from .external_api import fetch_objects, create_agent_if_available  # noqa
from .runtime_deployment import check_required_files, set_env_defaults  # noqa
