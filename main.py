import uvicorn
from fastapi import FastAPI

from db_connections.sqlite_conn import engine as sqlite_engine
from models import cloud_model
from routers.cloud_trail import cloud_route

app = FastAPI()

app.include_router(cloud_route)
cloud_model.SqliteBase.metadata.create_all(sqlite_engine)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="127.0.0.1",
                port=9000,
                log_level="info",
                reload=True)

