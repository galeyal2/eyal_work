from datetime import datetime
from typing import List

from pydantic import BaseModel


class CloudSchema(BaseModel):
    file_path: str

    class Config:
        arbitrary_types_allowed = True


class ShowCloudResult(BaseModel):
    event_id: str
    request_id: str
    event_type: str
    event_timestamp: datetime
    affected_assets: List[str]
    anomaly_score: int

    class Config:
        arbitrary_types_allowed = True
