import hashlib
import hmac
import json

from fastapi.testclient import TestClient
from forgeci.api.main import app

client = TestClient(app)

def test_github_webhook(monkeypatch):

    secret = "forgeci-test-secret"
    monkeypatch.setenv(
        "GITHUB_WEBHOOK_SECRET",
        secret
    )
    payload = {
        "ref": "refs/heads/main",
        "after": "abc123def456",
        "repository": {
            "full_name": "facchinimat/test-project"
        }
    }

    body = json.dumps(payload).encode()

    signature = (
        "sha256=" + hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
    )

    response = client.post(
        "/webhooks/github", 
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": signature
        }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Github webhook received"
    assert data["repository"] == "facchinimat/test-project"
    assert data["commit"] == "abc123def456"
    assert data["ref"] == "refs/heads/main"


def test_github_webhook_missing_signature(monkeypatch):
    monkeypatch.setenv(
        "GITHUB_WEBHOOK_SECRET",
        "forgeci-test-secret"
    )

    payload = {
        "ref": "refs/heads/main",
        "after": "abc123def456",
        "repository": {
            "full_name": "facchinimat/test-project"
        }
    }

    response = client.post(
        "/webhooks/github",
        json=payload
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Missing GitHub signature"

def test_github_webhook_invalid_signature(monkeypatch):
    monkeypatch.setenv(
        "GITHUB_WEBHOOK_SECRET",
        "forgeci-test-secret"
    )
    
    payload = {
        "ref": "refs/heads/main",
        "after": "abc123def456",
        "repository": {
            "full_name": "facchinimat/test-project"
        }
    }
    
    response = client.post(
        "/webhooks/github",
        json=payload,
        headers={
            "X-hub-Signature-256": "sha256=this-is-fake"
        }
    )

    assert response.status_code== 403
    assert response.json()["detail"]== "Invalid GitHub signature"