from sqlalchemy.orm import Session

from db_connections.sqlite_conn import SqliteBase
from utils.my_logger import orca_logger


def select_all_records(db: Session, table_model: SqliteBase):
    orca_logger.info("getting all anomaly result from target")
    return db.query(table_model).all()