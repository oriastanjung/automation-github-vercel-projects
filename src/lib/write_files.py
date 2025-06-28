import os
import asyncio

async def async_write_merged_files(merged_files: dict, uuid: str, base_dir="output", repo_name: str = "repo"):
    def sync_write():
        os.makedirs(base_dir, exist_ok=True)
        root_path = os.path.normpath(os.path.join(base_dir, uuid, repo_name))
        os.makedirs(root_path, exist_ok=True)
        for rel_path, content in merged_files.items():
            code = content.get("code")
            if code is None:
                continue
            normalized_path = os.path.normpath(os.path.join(root_path, rel_path))
            os.makedirs(os.path.dirname(normalized_path), exist_ok=True)
            with open(normalized_path, "w", encoding="utf-8") as f:
                f.write(code)
        return root_path

    final_path = await asyncio.to_thread(sync_write)
    print(f"✅ {len(merged_files)} files written to: {final_path}")
    return merged_files
