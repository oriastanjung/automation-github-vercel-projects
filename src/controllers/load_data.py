from src.lib.json import load_data


async def load_files_and_merge(file_path : str) -> dict:
    data = await load_data(file_path)
    workspace_files = data.get("workspace_generated_files", {})
    initial_files = data.get("initial_files", {})
    merged_files = {**initial_files, **workspace_files}  # workspace overwrite initial if conflict

    return merged_files