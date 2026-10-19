import os

os.environ.setdefault("CS_API_URL", "http://crowdsec.invalid/v1")
os.environ.setdefault("CS_API_KEY", "test-key")
os.environ.setdefault("CS_MACHINE_ID", "test-machine")
os.environ.setdefault("CS_MACHINE_PASSWORD", "test-password")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import app.api  # noqa: E402
import app.main  # noqa: E402

DECISIONS = [
    {
        "value": "203.0.113.7",
        "scope": "Ip",
        "type": "ban",
        "duration": "3h59m",
        "origin": "crowdsec",
        "scenario": "crowdsecurity/http-probing",
    }
]


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    async def fake_list_decisions() -> list[dict]:
        return DECISIONS

    monkeypatch.setattr(app.main, "list_decisions", fake_list_decisions)
    monkeypatch.setattr(app.api, "list_decisions", fake_list_decisions)
    return TestClient(app.main.app)


def test_index_renders_decisions(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert "203.0.113.7" in resp.text
    assert "crowdsecurity/http-probing" in resp.text


def test_api_lists_decisions(client: TestClient) -> None:
    resp = client.get("/api/decisions")
    assert resp.status_code == 200
    assert resp.json() == {"decisions": DECISIONS}


def test_api_delete_decision(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    deleted: list[str] = []

    async def fake_delete_decision(ip: str) -> None:
        deleted.append(ip)

    monkeypatch.setattr(app.api, "delete_decision", fake_delete_decision)
    resp = client.delete("/api/decisions/203.0.113.7")
    assert resp.status_code == 200
    assert resp.json() == {"status": "deleted", "ip": "203.0.113.7"}
    assert deleted == ["203.0.113.7"]
