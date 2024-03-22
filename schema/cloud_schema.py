from typing import List

from pydantic import BaseModel


class CloudSchema(BaseModel):
    file_path: str

    class Config:
        arbitrary_types_allowed = True


class ShowCloudResult(BaseModel):
    id: int
    event_id: str
    request_id: str
    event_type: str
    event_timestamp: str
    affected_assets: List[str]
    anomaly_score: int

    class Config:
        arbitrary_types_allowed = True
