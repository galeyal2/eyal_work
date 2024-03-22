from fastapi import HTTPException, status

from db_connections.sqlite_conn import get_db
from routers.utils.anomaly_func import process_chunk
from routers.utils.cloud_sqls import insert_tmp_into_target_sql
from routers.utils.handel_bulks import read_in_bulks
from routers.utils.manage_queue import generate_chunk_queue, generate_result_queue
from routers.utils.workers import create_workers


def event_process(file_source_path: str = 'sources'):
    file_chunks = read_in_bulks(file_source_path)
    chunk_queue = generate_chunk_queue(file_chunks)
    result_queue = generate_result_queue()

    all_success: bool = create_workers(target=process_chunk,
                                       chunk_queue=chunk_queue,
                                       result_queue=result_queue)

    if all_success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"one or more workers failed")


def insert_tmp_into_target():
    with get_db() as db:
        db.execute(
            insert_tmp_into_target_sql
        )
