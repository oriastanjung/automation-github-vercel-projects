import httpx
API_BASE = "https://api.vercel.com"

async def get_project(token: str, project_name: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/v9/projects/{project_name}", headers=headers)
        return r if r.status_code == 200 else None

async def create_project(token: str, project_name: str, repo: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": project_name,
        "gitRepository": {
            "type": "github",
            "repo": repo
        }
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/v9/projects", headers=headers, json=payload)
        if r.status_code in (200, 201):
            print(f"✅ Project created: {project_name}")
        else:
            print(f"❌ Failed to create project: {r.status_code} {r.text}")
        return r


async def trigger_deploy(
    token: str,
    project_name: str,
    files: list,
    deployment_id: str,
    git_metadata: dict,
    git_source: dict,
    meta: dict,
    monorepo_manager: str,
    project_settings: dict,
    custom_env_slug: str = None,
) -> tuple[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": project_name,
        "project": project_name,
        "target": "production",
        "files": files,
        "deploymentId": deployment_id,
        "gitMetadata": git_metadata,
        "gitSource": git_source,
        "meta": meta,
        "monorepoManager": monorepo_manager,
        "projectSettings": project_settings,
        "withLatestCommit": True,
    }

    if custom_env_slug:
        payload["customEnvironmentSlugOrId"] = custom_env_slug

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/v13/deployments", headers=headers, json=payload)
        if r.status_code in (200, 201):
            json_data = r.json()
            deploy_url = r.json().get("url")
            vercel_deployment_id = json_data.get("id")
            print(f"🚀 Deployment triggered: https://{deploy_url}")
            return f"https://{deploy_url}", vercel_deployment_id
        else:
            print(f"❌ Deployment failed: {r.status_code} {r.text}")
            return None



async def get_deployment_status(token: str, deployment_id: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/v13/deployments/{deployment_id}", headers=headers)
        return r.json()