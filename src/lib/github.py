import aiohttp
import subprocess
import asyncio
from config import config
import httpx

async def create_new_repo_async(token: str, repo_name: str, private: bool = True, description: str = "Auto-generated repository") -> str:
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "name": repo_name,
        "private": private,
        "description": description,
        "auto_init": False
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status == 201:
                response_data = await resp.json()
                # print(f"✅ Repo created: {response_data['html_url']}")
                return response_data["clone_url"]
            else:
                text = await resp.text()
                if "already exists" in text.lower():
                    clone_url = f"https://github.com/{config.github_username}/{repo_name}.git"
                    # print(f"⚠️  Repo already exists: {clone_url}")
                    return clone_url
                raise Exception(f"GitHub repo creation failed: {resp.status}")
async def push_repo_force_async(folder_path: str, repo_url_with_auth: str, branch: str = "main", commit_msg: str = "Initial commit"):
    """
    Push isi folder ke repo GitHub dengan force. Abaikan GPG signing, dan commit dummy jika tidak ada perubahan.
    """
    def sync_git_commands():
        # print(f"📂 Git folder path: {folder_path}")

        # Debug: tampilkan isi folder
        # print("📄 File yang ditemukan sebelum git init:")
        # for root, dirs, files in os.walk(folder_path):
        #     for file in files:
                # print(" -", os.path.relpath(os.path.join(root, file), folder_path))

        # Inisialisasi Git repo dan konfig
        init_cmds = [
            ['git', 'init'],
            ['git', 'checkout', '-B', branch],
            ['git', 'config', 'commit.gpgSign', 'false'],
            ['git', 'add', '.']
        ]
        for cmd in init_cmds:
            subprocess.run(cmd, cwd=folder_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Debug status
        subprocess.run(['git', 'status'], cwd=folder_path)

        # Cek apakah ada staged file
        has_changes = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=folder_path)
        if has_changes.returncode == 0:
            # print("⚠️  No changes to commit. Creating dummy commit to force push.")
            subprocess.run(['git', 'commit', '--allow-empty', '-m', f"{commit_msg} (force)"], cwd=folder_path, check=True)
        else:
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=folder_path, check=True)

        # 🛠️ Pastikan remote origin diset ulang (hindari error)
        subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=folder_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url_with_auth], cwd=folder_path, check=True)

        # 🚀 Push pakai force
        subprocess.run(['git', 'push', '-f', 'origin', branch], cwd=folder_path, check=True)

    # Jalankan secara asynchronous
    try:
        await asyncio.to_thread(sync_git_commands)
        # print(f"🚀 Success: pushed to {repo_url_with_auth}")
    except subprocess.CalledProcessError as e:
        # print("❌ Git push failed:")
        print(e.stderr.decode() if e.stderr else str(e))


async def get_github_repo_id(repo_fullname: str, github_token: str) -> int:
    """
    Example: repo_fullname = "altariapp/userId_project-4"
    """
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.github.com/repos/{repo_fullname}", headers=headers)
        r.raise_for_status()
        return r.json()["id"]

