import queue
import threading
from typing import Callable

from utils.my_logger import orca_logger

num_workers = 3


def create_workers(target: Callable,
                   chunk_queue: queue.Queue,
                   result_queue: queue.Queue) -> bool:

    threads = []
    worker_status = {}  # Dictionary to store the status of each worker thread
    for i in range(num_workers):
        orca_logger.info(f"Init worker number: {i}")
        thread = threading.Thread(target=worker_wrapper,
                                  args=(i, target, chunk_queue, result_queue, worker_status)
                                  )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return check_worker_status(worker_status, num_workers)


def worker_wrapper(worker_id: int,
                   target: Callable,
                   chunk_queue: queue.Queue,
                   result_queue: queue.Queue,
                   worker_status: dict) -> None:

    try:
        print("eyal")
        # worker_status[worker_id] = True
        chunk = chunk_queue.get()
        # # result = target(worker_id,
        # #                 chunk,
        # #                 result_queue)
        worker_status[worker_id] = True

        # if result == -1:
        #     worker_status[worker_id] = False  # Indicate failure
        # else:
        #     worker_status[worker_id] = True  # Indicate success
    except Exception as e:
        pass
        # orca_logger.error(f"Worker {worker_id} failed: {str(e)}")
        # worker_status[worker_id] = False


def check_worker_status(worker_status: dict, num_workers: int) -> bool:
    for i in range(num_workers):
        if not worker_status.get(i, False):
            orca_logger.error(f"Worker {i} failed")
            return False
    return True
