import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()

# === CONFIGURATION ===
REPO_NAME = "diesel-codex-56.com"
GITHUB_USERNAME = "Diesel56"
BRANCH = "main"
REMOTE_NAME = "origin"

# Read GitHub token securely from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_PAT")
if not GITHUB_TOKEN:
    raise EnvironmentError("Missing GitHub token. Please set GITHUB_PAT in your environment or .env file.")

# Define the repo HTTPS URL using token
REMOTE_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# Set Git remote URL
subprocess.run(["git", "remote", "set-url", REMOTE_NAME, REMOTE_URL], check=True)

# Git add, commit, and push
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "🚀 Auto-deployed Diesel Drop with secure token"], check=True)
subprocess.run(["git", "push", REMOTE_NAME, BRANCH], check=True)

print("✅ Deployment complete.")
