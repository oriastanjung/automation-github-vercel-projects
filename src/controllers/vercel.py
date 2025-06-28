import asyncio
from src.lib.vercel import (
    get_project,
    create_project,
    trigger_deploy,
    get_deployment_status,
)
from src.lib.github import get_github_repo_id
from config import config
from src.utils.sanitize_project_name import sanitize_project_name
from src.utils.extract_repo_name import extract_repo_name
from src.utils.vercel_helper import (
    generate_vercel_files_payload,
    generate_deployment_id,
    generate_git_metadata,
    generate_git_source,
    generate_meta,
    generate_monorepo_manager,
    generate_project_settings,
)


async def deploy_to_vercel(
    project_name: str, github_repo: str, folder_path: str, repo_name: str, files: dict
) -> str:
    token = config.vercel_token
    github_token = config.github_pat_token
    # generate vercel files payload
    project_name = await sanitize_project_name(project_name)
    repo_name = await extract_repo_name(repo_name)
    repo_id = await get_github_repo_id(
        repo_fullname=repo_name, github_token=github_token
    )
    files = await generate_vercel_files_payload(files)
    deployment_id = await generate_deployment_id(project_name)
    git_metadata = await generate_git_metadata(project_name)
    git_source = await generate_git_source(repo_id)
    meta = await generate_meta(project_name)
    monorepo_manager = await generate_monorepo_manager()
    project_settings = await generate_project_settings()

    exists = await get_project(token, project_name)
    if not exists:
        await create_project(token, project_name, repo_name)
    deployment_vercel_url, vercel_deployment_id = await trigger_deploy(
        deployment_id=deployment_id,
        files=files,
        git_metadata=git_metadata,
        git_source=git_source,
        meta=meta,
        monorepo_manager=monorepo_manager,
        project_name=project_name,
        project_settings=project_settings,
        token=token,
    )
    # get status of deployment, if its success, return the hosted vercel url
    hosted_vercel_url = None
    is_error = False
    while True:
        status_data = await get_deployment_status(token, vercel_deployment_id)
        status = status_data.get("readyState")
        if status == "READY":
            break
        elif status == "ERROR":
            is_error = True
            break
        print("Deployment is not ready, waiting for 5 seconds")
        await asyncio.sleep(5)
    if is_error:
        return None, None, is_error
    hosted_vercel_url = f"https://{project_name}.vercel.app"
    return deployment_vercel_url, hosted_vercel_url, is_error
