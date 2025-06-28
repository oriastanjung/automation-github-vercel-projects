import json
import asyncio

    
async def load_data(file_path) -> dict:
    def _load_data(file_path) -> dict:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    return await asyncio.to_thread(_load_data, file_path)


async def save_data(file_path, data) -> None:
    def _save_data(file_path, data):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    return await asyncio.to_thread(_save_data, file_path, data)