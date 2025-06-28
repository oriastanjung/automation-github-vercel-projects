from src.lib.github import create_new_repo_async, push_repo_force_async
from config import config
from datetime import datetime

async def create_and_push_repo(
    repo_name: str,
    folder_path: str,
    branch: str = "main",
):
    repo_url = await create_new_repo_async(
        token=config.github_pat_token, repo_name=repo_name
    )
    repo_url_with_auth = repo_url.replace(
        "https://",
        f"https://{config.github_username}:{config.github_pat_token}@"
    )
    commit_msg = f"Commit for {repo_name} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    await push_repo_force_async(
        folder_path=folder_path,
        repo_url_with_auth=repo_url_with_auth,
        branch=branch,
        commit_msg=commit_msg,
    )

    return repo_url, repo_url_with_auth
