from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from db_connections.sqlite_conn import get_db_for_repo
from models.cloud_model import CloudEvent
from repositories.sqlite_repo import select_all_records
from routers.utils.main_process import event_process, insert_tmp_into_target
from schema.cloud_schema import ShowCloudResult

cloud_route = APIRouter(
    tags=['cloud_trail'],
    prefix='/cloud'
)


@cloud_route.get("/run", status_code=status.HTTP_200_OK)
async def cloud_process(file_source_path: str = 'sources'):
    event_process(file_source_path)
    insert_tmp_into_target()
    return {"message": f"events were processed inserted to the db"}


@cloud_route.get(path='/', response_model=List[ShowCloudResult])
async def get_annomaly(db: Session = Depends(get_db_for_repo)):
    return select_all_records(table_model=CloudEvent, db=db)
