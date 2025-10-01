# tests/test_external_api.py
import json
import types
import pytest

from strands_agentcore.external_api import get_objects_api, strands_agent_bedrock


class DummyResponse:
    def __init__(self, ok_json, status_code=200):
        self._json = ok_json
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP error")


def test_get_objects_api_success(monkeypatch):
    expected = {"objects": [{"id": 1, "name": "foo"}]}

    def fake_get(url, verify, timeout):
        return DummyResponse(expected)

    monkeypatch.setattr("strands_agentcore.external_api.requests.get", fake_get)
    result = get_objects_api()
    assert result == expected


def test_strands_agent_bedrock_no_prompt():
    res = strands_agent_bedrock({"prompt": ""})
    assert res == "No prompt provided"


def test_strands_agent_bedrock_with_agent():
    res = strands_agent_bedrock({"prompt": "hello"})
    # Adjust assertion depending on the real implementation
    assert res is not None
    assert isinstance(res, str)
