import json
import httpx

from fastapi import FastAPI, HTTPException
from typing import Any, Dict
from pathlib import Path
from Models import *

app = FastAPI(title="Storage API")
        
storages = {}

@app.post("/register")
async def register_storage(user_data: StorageRegistration):
    if user_data.name in storages.keys():
        return {
            "Status": "Failure",
            "message": "name is occupied"
        }

    storages[user_data.name] = StorageData(user_data.source_url)
    
    return {
        "status": "Success",
        "message": f"Storage {user_data.name} registered",
        "source_url": user_data.source_url
    }

@app.get("/{storage_name}")
async def get_storage(storage_name: str):
    storage = storages.get(storage_name)

    if storage is None:
        return {
            "status": "Error",
            "message": "storage not found"
        }

    if storage.source_url:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(storage.source_url)
                response.raise_for_status()
                return response.json()
            except Exception as ex:
                raise HTTPException(503, detail=f"Failed to get data {storage.source_url}: {ex}")
    
    return storage.data

@app.post("/{storage_name}")
async def update_storage(storage_name: str, data: Dict[str, Any]):
    if storage_name not in storages.keys():
        return {
            "status": "Error",
            "message": "storage not found"
        }

    storages[storage_name].data = data
    return {"status": "Success", "updated_storage": storage_name}


@app.get("/mock/board/{board_type}")
async def get_board_data(board_type):
    file = Path('./boards') / f"{board_type}.json"
    if not file.exists():
        return {"error": "wrong board type"}
 
    with open(file) as source:
        data = json.load(source)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)