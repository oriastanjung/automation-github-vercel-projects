import base64
import hashlib
import uuid
from typing import List, Dict
from datetime import datetime
import os

async def generate_vercel_files_payload(merged_files: dict) -> List[Dict[str, str]]:
    files = []

    for path, content in merged_files.items():
        # Normalisasi path
        clean_path = os.path.normpath(path).replace("\\", "/").lstrip("./")

        # Hilangkan ../ dan karakter spesial berbahaya
        if ".." in clean_path or clean_path.startswith("/"):
            continue  # Skip path yang tidak valid

        code = content.get("code", "")
        encoded = base64.b64encode(code.encode("utf-8")).decode("utf-8")

        files.append({
            "file": clean_path,
            "data": encoded,
            "encoding": "base64"
        })

    return files


async def generate_deployment_id(project_name: str) -> str:
    # Vercel-style: dpl_<hash>
    raw = f"{project_name}_{uuid.uuid4()}"
    hashed = hashlib.sha1(raw.encode()).hexdigest()[:20]
    return f"dpl_{hashed}"


async def generate_git_metadata(project_name: str) -> dict:
    return {
        "remoteUrl": f"https://github.com/altariapp/{project_name}",
        "commitAuthorName": "auto-deployer",
        "commitMessage": f"Deploy {project_name} via API",
        "commitRef": "main",
        "commitSha": "main",
        "dirty": True
    }


async def generate_git_source(repo_id: int) -> dict:
    return {
        "ref": "main",
        "sha": "main",
        "type": "github",
        "repoId": repo_id
    }


async def generate_meta(project_name: str) -> dict:
    return {
        "project": project_name,
        "env": "production"
    }


async def generate_monorepo_manager() -> str:
    return "npm"  # or "npm", "yarn", etc. if using monorepo tooling; adjust if not needed


async def generate_project_settings() -> dict:
    return {
        "buildCommand": "next build",
        "devCommand": "next dev",
        "installCommand": "npm install",
        "framework": "nextjs",
        "outputDirectory": ".next",
        "skipGitConnectDuringLink": True,
        "sourceFilesOutsideRootDirectory": False
    }
