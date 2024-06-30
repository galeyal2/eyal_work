import random
from asyncio import Lock, get_event_loop
from collections import defaultdict

from sqlalchemy import text

from db_connections.sqlite_conn import get_db
from routers.utils.lfu import LFUCache
from utils.my_logger import orca_logger

# Initialize the LFU cache as a global variable
lfu_cache = LFUCache(capacity=100_000)

# Create a dictionary to store locks for each event loop
lfu_cache_locks = defaultdict(Lock)


async def process_chunk(worker_number: int, chunk, result_queue):
    """
    Process a chunk of data and put the results in the result_queue.
    """
    orca_logger.info(f"Worker number {worker_number} started processing.")
    results = []
    for event in chunk:
        processed_event = await process_event(event)
        if processed_event is not None:
            results.append(processed_event)
    orca_logger.info("Worker finished processing.")
    result_queue.put(results)
    insert_events_in_db(results)


async def process_event(event):
    event_loop = get_event_loop()
    async with lfu_cache_locks[event_loop]:
        anomaly_score = random.randint(0, 1)
        event_id = event['event_id']

        event_frequency = lfu_cache.get(event_id)

        if event_frequency is None:
            lfu_cache.put(event_id, 1)
        else:
            lfu_cache.put(event_id, event_frequency + 1)
        # Check if the event has been processed more than 5 times
        if lfu_cache.get(event_id) > 5:
            anomaly_score = fetch_anomaly_score_from_db(event_id)
            if anomaly_score == -1:
                anomaly_score = random.randint(0, 1)
        event['anomaly_score'] = anomaly_score

        if event['anomaly_score'] == 1:
            return event
        else:
            return None


def insert_events_in_db(events):
    with get_db() as db:
        try:
            db.execute(
                text("INSERT INTO cloud_events_tmp (event_id, "
                     "request_id, "
                     "event_type, "
                     "event_timestamp, "
                     "affected_assets, "
                     "anomaly_score)"
                     " VALUES (:event_id, :request_id, :event_type, :event_timestamp, :affected_assets, :anomaly_score)"),
                [{
                    'event_id': event['event_id'],
                    'request_id': event['request_id'],
                    'event_type': event['event_type'],
                    'event_timestamp': str(event['event_timestamp']),
                    'affected_assets': event['affected_assets'],
                    'anomaly_score': event['anomaly_score']
                } for event in events]
            )
        except Exception as e:
            raise e

        # Ensure the function returns an object
        return True


def fetch_anomaly_score_from_db(event_id):
    with get_db() as db:
        result = db.execute(text(f"SELECT anomaly_score FROM cloud_events WHERE event_id=:event_id"),
                            {"event_id": event_id})
        row = result.fetchone()
        if row:
            return row[0]
        else:
            return None
