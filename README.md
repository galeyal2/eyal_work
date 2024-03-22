# Cloud Event Processing Project

This project provides functionality for processing cloud events, storing them in a SQLite database, and exposing APIs to
interact with the processed data.

## Table of Contents

- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

├── db_connections
│ └── sqlite_conn.py
├── models
│ └── cloud_model.py
├── repositories
│ └── sqlite_repo.py
├── routers
│ ├── cloud_trail.py
│ └── utils
│ ├── anomaly_func.py
│ ├── handel_bulks.py
│ ├── main_process.py
│ ├── manage_queue.py
│ └── workers.py
└── schema
└── cloud_schema.py

The project is organized into different directories:

- `db_connections`: Contains the SQLite database connection module.
- `models`: Defines SQLAlchemy models for cloud events.
- `repositories`: Provides repository functions for interacting with the database.
- `routers`: Contains FastAPI routers for handling HTTP requests.
- `schema`: Defines Pydantic schemas for request and response payloads.

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Faker](https://faker.readthedocs.io/)

## Installation For Manual Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/galeyal2/eyal_orca.git
   ```
2. **Install the dependencies**:
   ```bash 
   pip install -r requirements.txt
   ```

3. **run Faker to create fake records**:
   ```bash
   python sources/create_faker_events.py
   ```

4. **Start the FastAPI server**:
   [run_requests.http](run_requests.http)
   ```bash
   uvicorn main:app --host=127.0.0.1 --port=9000 --log-level=info --reload
   ```
## Docker

1. **build docker image**:

   ```bash
   docker build -t eyal_orca -f dockerfile .
   ```
2. **run docker image**
   ```bash
   docker run -p 9000:9000 --rm eyal_orca
   ```
   
# Run HTTP
   [run_requests.http](run_requests.http)

## Event Processing

The `event_process(file_source_path)` function is responsible for processing cloud events from a specified file source
path and storing them in the database. Here's a breakdown of how it works:

1. **Reading Data**:
    - The function starts by reading data from the specified file source path. This data usually comprises bulk cloud
      events stored in a CSV file format.

2. **Chunk Processing**:
    - To optimize memory usage, the function processes the data in manageable chunks. Each chunk of data is processed
      independently, allowing for more efficient processing.

3. **Queue Management**:
    - Efficient data processing is ensured through queue management. The function generates a queue of chunks to be
      processed and a result queue to store the processed results.

4. **Worker Creation**:
    - Concurrent processing is facilitated by creating worker threads, each tasked with processing a chunk of data. This
      parallelization enhances performance by distributing the processing load across multiple threads.

5. **Processing**:
    - Each worker thread processes its assigned chunk of data by executing a predefined set of processing tasks defined
      in the `anomaly_func.py` module. These tasks may include generating anomaly scores for events, updating event
      counts, and inserting events into the database.

6. **Error Handling**:
    - Error handling is implemented to gracefully manage any encountered errors during processing. If a worker thread
      encounters an error, it is logged, and the overall processing status is appropriately updated.

7. **Database Insertion**:
    - Upon processing all chunks of data, the function proceeds to insert the processed events into the SQLite database
      using the `insert_tmp_into_target()` function.

8. **Completion Status**:
    - Finally, the function verifies the status of all worker threads. If any worker thread fails to process its chunk
      successfully, an HTTP exception is raised, indicating that one or more workers have failed.

