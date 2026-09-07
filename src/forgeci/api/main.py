from fastapi import FastAPI

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
async def github_webhook(payload: dict):

    repository = payload.get("repository", {})
    repo_name = repository.get("full_name")

    commit_sha = payload.get("after")
    branch = payload.get("ref")

    return {
        "message": "Github webhook received",
        "repository": repo_name,
        "commit": commit_sha,   #secure hash algorithm 
        "ref": branch
    }

