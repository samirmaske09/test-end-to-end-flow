# tests/test_external_api.py
import json
import types
import pytest

from strands_agentcore.external_api import get_objects_api, handler

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

def test_handler_no_prompt(monkeypatch):
    # provide a dummy agent that shouldn't be called
    dummy_agent = lambda prompt: "should not be called"
    res = handler({"prompt": ""}, agent=dummy_agent)
    assert res == "No prompt provided"

def test_handler_with_agent(monkeypatch):
    dummy_agent = lambda prompt: "ok:" + prompt
    res = handler({"prompt": "hello"}, agent=dummy_agent)
    assert res == "ok:hello"
