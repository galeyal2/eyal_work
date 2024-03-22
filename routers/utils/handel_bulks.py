import os


def read_in_bulks(data_source: str = "sources", num: int = 1000):
    file_path = os.path.join(data_source, 'fake_cloud_events.csv')
    with open(file_path, "r") as f:
        next(f)  # skip the header
        while True:
            chunk = []
            try:
                for _ in range(num):
                    line = next(f)
                    chunk.append(line.strip().split(','))
            except StopIteration:
                if chunk:
                    yield chunk
                break
            yield chunk
