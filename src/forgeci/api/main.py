from fastapi import FastAPI, HTTPException, Request
import hashlib
import hmac
import os
import json

app = FastAPI(
    title = "ForgeCI",
    version = "0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "forgeci-api"
    }


@app.post("/webhooks/github")
async def github_webhook(request: Request):

    body = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")

    verify_github_signature(body, signature)

    event = request.headers.get("X-GitHub-Event")

    if not event:
        raise HTTPException(
            status_code = 400,
            detail = "Missing GitHub event type"
        )

    if event != "push":
        return {
            "message": "GitHub event ingored",
            "event": event
        }

    payload = json.loads(body)

    repository = payload.get("repository", {})
    repo_name = repository.get("full_name")

    commit_sha = payload.get("after")
    branch = payload.get("ref")

    return {
        "message": "GitHub push received",
        "repository": repo_name,
        "commit": commit_sha,   #secure hash algorithm 
        "ref": branch
    }

#helper function to check if webhook request came from GitHub
def verify_github_signature(body: bytes, signature: str | None):
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")

    if not secret:
        raise HTTPException(
            status_code = 500,
            detail = "GitHub webhook secret is not configured"
        )

    if not signature:
        raise HTTPException(
            status_code= 403,
            detail = "Missing GitHub signature"
        )
    #github webhook signature format uses HMAC with SHAH-256
    expected_signature = (
        "sha256=" + hmac.new(
            secret.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
    )

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(
            status_code = 403,
            detail= "Invalid GitHub signature"
        )