import csv
import os.path
import random
from datetime import timezone

from faker import Faker

fake = Faker()

same_event_ids = ["same_event_id1", "same_event_id2"]


def generate_fake_event_id() -> str:
    return random.choice(same_event_ids) if random.random() < 0.2 else fake.uuid4()


def generate_fake_data_csv(file_path, num_records):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['event_id', 'request_id', 'event_type', 'event_timestamp', 'affected_assets']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(num_records):
            event_id = generate_fake_event_id()
            request_id = fake.uuid4()
            event_type = fake.word()
            event_timestamp = fake.date_time_this_decade(tzinfo=timezone.utc)
            affected_assets = [str(word) for word in fake.words()]

            # Write to CSV
            writer.writerow({'event_id': event_id, 'request_id': request_id, 'event_type': event_type,
                             'event_timestamp': event_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                             'affected_assets': affected_assets})


file_name = 'fake_cloud_events.csv'
file_location = '.' if 'sources' in os.getcwd() else './sources'
file_path = os.path.join(file_location, file_name)

generate_fake_data_csv(file_path, 10_000)
