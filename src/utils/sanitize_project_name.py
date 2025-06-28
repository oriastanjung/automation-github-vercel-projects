import re
import asyncio
async def sanitize_project_name(name: str) -> str:
    def _sanitize_project_name(name: str) -> str:
        name = name.lower()
        name = re.sub(r"[^a-z0-9._-]+", "-", name)
        name = re.sub(r"-{2,}", "-", name)
        return name.strip("-")

    return await asyncio.to_thread(_sanitize_project_name, name)
