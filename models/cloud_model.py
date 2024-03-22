import json

from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator, ARRAY

from db_connections.sqlite_conn import SqliteBase


class ArrayString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                print("Value causing error:", value)
                return None
        return None



class CloudEventTemp(SqliteBase):
    __tablename__ = 'cloud_events_tmp'

    id = Column(Integer, primary_key=True)
    event_id = Column(String(255))
    request_id = Column(String(255))
    event_type = Column(String(255))
    event_timestamp = Column(DateTime)
    affected_assets = Column(ARRAY(String))
    anomaly_score = Column(Integer)


class CloudEvent(SqliteBase):
    __tablename__ = 'cloud_events'

    event_id = Column(String(255), primary_key=True)
    request_id = Column(String(255))
    event_type = Column(String(255))
    event_timestamp = Column(DateTime)
    affected_assets = Column(ARRAY(String))
    anomaly_score = Column(Integer)
