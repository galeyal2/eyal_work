import queue
import threading
import asyncio
from typing import Callable, Awaitable

from routers.utils.anomaly_func import lfu_cache
from utils.my_logger import orca_logger

num_workers = 3


async def async_worker_wrapper(worker_id: int,
                               target: Callable[..., Awaitable],
                               chunk_queue: queue.Queue,
                               result_queue: queue.Queue,
                               worker_status: dict) -> None:
    try:
        chunk = chunk_queue.get(timeout=10)
        result = await target(worker_id, chunk, result_queue)

        if result == -1:
            worker_status[worker_id] = False  # Indicate failure
        else:
            worker_status[worker_id] = True  # Indicate success
    except queue.Empty:
        orca_logger.error(f"Worker {worker_id} timed out while waiting for chunk.")
        worker_status[worker_id] = True
    except Exception as e:
        orca_logger.error(f"Worker {worker_id} failed: {str(e)}")
        worker_status[worker_id] = False


def worker_wrapper(worker_id: int,
                   target: Callable[..., Awaitable],
                   chunk_queue: queue.Queue,
                   result_queue: queue.Queue,
                   worker_status: dict) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_worker_wrapper(worker_id, target, chunk_queue, result_queue, worker_status))


def create_workers(target: Callable,
                   chunk_queue: queue.Queue,
                   result_queue: queue.Queue) -> bool:
    threads = []
    worker_status = {}
    for i in range(num_workers):
        orca_logger.info(f"Init worker number: {i}")
        thread = threading.Thread(target=worker_wrapper,
                                  args=(i, target, chunk_queue, result_queue, worker_status)
                                  )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    lfu_cache.cache.clear()
    return check_worker_status(worker_status, num_workers)


def check_worker_status(worker_status: dict, num_workers: int) -> bool:
    for i in range(num_workers):
        if not worker_status.get(i, False):
            orca_logger.error(f"Worker {i} failed")
            return False
    return True
