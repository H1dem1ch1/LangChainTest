import os
import hmac
import hashlib
from typing import Dict

from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

from main import perform_review

app = FastAPI()

load_dotenv()
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

@app.post("/webhook")
async def github_webhook(request: Request):
    if WEBHOOK_SECRET:
        # Verify webhook signature
        signature = request.headers.get("X-Hub-Signature-256")
        if not signature:
            raise HTTPException(status_code=401, detail="X-Hub-Signature-256 header missing")

        body = await request.body()
        hash_object = hmac.new(WEBHOOK_SECRET.encode("utf-8"), msg=body, digestmod=hashlib.sha256)
        expected_signature = "sha256=" + hash_object.hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            raise HTTPException(status_code=401, detail="Webhook signature mismatch")

    event = request.headers.get("X-GitHub-Event")
    payload: Dict = await request.json()

    if event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "reopened", "synchronize"]:
            repo_name = payload["repository"]["full_name"]
            pr_number = payload["pull_request"]["number"]
            print(f"Received pull_request event for {repo_name}#{pr_number} (action: {action})")
            
            # Perform review in a background task if needed for long-running tasks
            # For now, directly call perform_review
            perform_review(repo_name, pr_number)
            return {"message": "Review initiated"}
    
    return {"message": f"Event {event} with action {payload.get('action')} ignored"}

