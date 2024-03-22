from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator

from db_connections.sqlite_conn import SqliteBase


class ArrayString(TypeDecorator):
    """
    Custom type decorator for storing a list of strings in SQLite.
    """

    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return ', '.join(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.split(', ')
        return None


class CloudEventTemp(SqliteBase):
    __tablename__ = 'cloud_events_tmp'

    id = Column(Integer, primary_key=True)
    event_id = Column(String(255))
    request_id = Column(String(255))
    event_type = Column(String(255))
    event_timestamp = Column(DateTime)
    affected_assets = Column(ArrayString)
    anomaly_score = Column(Integer)


class CloudEvent(SqliteBase):
    __tablename__ = 'cloud_events'

    event_id = Column(String(255), primary_key=True)
    request_id = Column(String(255))
    event_type = Column(String(255))
    event_timestamp = Column(DateTime)
    affected_assets = Column(ArrayString)
    anomaly_score = Column(Integer)
