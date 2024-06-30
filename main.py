import os

import redis
import uvicorn
from fastapi import FastAPI

from db_connections.sqlite_conn import engine as sqlite_engine
from models import cloud_model
from routers.cloud_trail import cloud_route

app = FastAPI()

app.include_router(cloud_route)
cloud_model.SqliteBase.metadata.create_all(sqlite_engine)

# Get Redis connection details from environment variables
redis_host = os.getenv('REDIS_HOST', 'eyal-redis-server')
redis_port = int(os.getenv('REDIS_PORT', 6379))
print(os.environ)
# Connect to the Redis server
client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
# client = redis.StrictRedis(host='localhost', port=redis_port, decode_responses=True)


client.set('key', 'value')

# Get the value back from the Redis server
value = client.get('key')
print(f'The value of "key" is: {value}')

# Set a value in the Redis server
client.set('key', 'value')

# Get the value back from the Redis server
value = client.get('key')
print(os.getenv)


print(f'The value of "key" is: {value}')
print(f'The value of "key" is: {value}')
print(f'The value of "key" is: {value}')
print(f'The value of "key" is: {value}')
print(f'The value of "key" is: {value}')
print(f'The value of "key" is: {value}')


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=9000,
                log_level="info",
                reload=True)

