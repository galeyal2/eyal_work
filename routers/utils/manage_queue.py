import queue

from utils.my_logger import orca_logger


def generate_chunk_queue(file_chunks):
    chunk_queue = queue.Queue()
    # Read data and put into chunk queue FIFO
    for chunk in file_chunks:
        orca_logger.info("Processing a bulk of data.")
        chunk_queue.put(chunk)
    return chunk_queue


def generate_result_queue():
    orca_logger.info("create new queue")
    return queue.Queue()
