import random
from collections import defaultdict

from db_connections.sqlite_conn import get_db
from utils.my_logger import orca_logger


def process_chunk(worker_number:int, chunk, result_queue):
    """
    Process a chunk of data and put the results in the result_queue.
    """
    orca_logger.info(f"Worker number {worker_number} started processing.")
    results = []
    for event in chunk:
        event = process_event(event)
        results.append(event)
    orca_logger.info("Worker finished processing.")
    result_queue.put(results)


def process_event(event):
    processed_events = defaultdict(int)
    anomaly_score = random.randint(0, 1)
    event_id = event['event_id']

    # Update count for the event ID
    processed_events[event_id] += 1

    # Check if the event has been processed more than 5 times
    if processed_events[event_id] > 5:
        anomaly_score = fetch_anomaly_score_from_db(event_id)
        if anomaly_score is None:
            anomaly_score = random.randint(0, 1)
    event[anomaly_score] = anomaly_score
    return event


def insert_event_in_db(event):
    with get_db() as db:
        db.execute(
            "INSERT INTO events (event_id, request_id, event_type, event_timestamp, affected_assets, anomaly_score) VALUES (?, ?, ?, ?, ?, ?)",
            (event['event_id'], event['request_id'], event['event_type'], event['event_timestamp'],
             ','.join(event['affected_assets']), event['anomaly_score'])
        )


def fetch_anomaly_score_from_db(event_id):
    with get_db() as db:
        result = db.execute("SELECT anomaly_score FROM anomaly_results WHERE event_id=?", (event_id,))
        return result.fetchone()[0] if result else None
