from pydantic import BaseModel

from models.cloud_model import ArrayString


class CloudSchema(BaseModel):
    file_path: str


class ShowCloudResult(BaseModel):
    id: int
    event_id: str
    request_id: str
    event_type: str
    event_timestamp: str
    affected_assets: ArrayString
    anomaly_score: int

    class Config():
        from_attributes = True
