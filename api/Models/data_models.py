from typing import Any, Dict, Optional
from pydantic import BaseModel

class StorageRegistration(BaseModel):
    name: str 
    source_url: Optional[str] = None

class StorageData:
    source_url: str 
    data: Dict[str, Any]

    def __init__(self, source_url:Optional[str] = None):
        self.source_url = source_url
        self.data = {}