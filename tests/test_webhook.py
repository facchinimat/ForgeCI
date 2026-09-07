from fastapi.testclient import TestClient
from forgeci.api.main import app

client = TestClient(app)

def test_github_webhook():
    payload = {
        "ref": "refs/heads/main",
        "after": "abc123def456",
        "repository": {
            "full_name": "facchinimat/test-project"
        }
    }

    response = client.post("/webhooks/github", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Github webhook received"
    assert data["repository"] == "facchinimat/test-project"
    assert data["commit"] == "abc123def456"
    assert data["ref"] == "refs/heads/main"
