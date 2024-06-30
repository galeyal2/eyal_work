from fastapi import HTTPException, status

from db_connections.sqlite_conn import run_query
from routers.utils.anomaly_func import process_chunk
from routers.utils.cloud_sqls import truncate_tmp_table
from routers.utils.handel_bulks import read_in_bulks
from routers.utils.manage_queue import generate_chunk_queue, generate_result_queue
from routers.utils.workers import create_workers


def event_process(file_source_path: str = 'sources'):
    file_chunks = read_in_bulks(file_source_path)
    chunk_queue = generate_chunk_queue(file_chunks)
    result_queue = generate_result_queue()
    run_query(truncate_tmp_table)  # truncate temp table
    all_success: bool = create_workers(target=process_chunk,
                                       chunk_queue=chunk_queue,
                                       result_queue=result_queue)

    if not all_success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"one or more workers failed")
