import shutil
from src.controllers.load_data import load_files_and_merge
from src.lib.write_files import async_write_merged_files
from src.controllers.github import create_and_push_repo
from src.controllers.vercel import deploy_to_vercel
from src.utils.delete_project import on_rm_error


async def automatic_deployment(
    json_file_path: str, uuid: str, repo_name: str
) -> tuple[str, str, bool] | None:
    # load and merge data
    data = await load_files_and_merge(json_file_path)
    # write merged files
    merged_files = await async_write_merged_files(
        merged_files=data, uuid=uuid, repo_name=repo_name
    )

    # create and push repo
    repo_url, repo_url_with_auth = await create_and_push_repo(
        repo_name=f"{uuid}_{repo_name}", folder_path=f"output/{uuid}/{repo_name}"
    )

    # deploy to vercel
    deployment_vercel_url, hosted_vercel_url, is_error = await deploy_to_vercel(
        repo_name=repo_url,
        project_name=f"{uuid}{repo_name}",
        github_repo=repo_url_with_auth,
        folder_path=f"output/{uuid}/{repo_name}",
        files=merged_files,
    )
    
    # delete output folder
    shutil.rmtree(f"output/{uuid}/{repo_name}", onerror=on_rm_error)
    return deployment_vercel_url, hosted_vercel_url, is_error
