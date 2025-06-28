from urllib.parse import urlparse
import asyncio

async def extract_repo_name(repo_url: str) -> str:
    def _extract_repo_name(repo_url: str) -> str:
        parsed = urlparse(repo_url)
        path = parsed.path.lstrip('/')
        return path.removesuffix('.git')
    return await asyncio.to_thread(_extract_repo_name, repo_url)