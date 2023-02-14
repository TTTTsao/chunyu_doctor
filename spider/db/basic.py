import os
import threading

from sqlalchemy import (
    create_engine, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

from spider.config.conf import get_db_args
from contextlib import contextmanager

local = threading.local()

def get_engine():
    args = get_db_args()
    password = os.getenv('DB_PASS', args['password'])
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(args['db_type'], args['user'], password,
                                                             args['host'], args['port'], args['db_name'])
    engine = create_engine(connect_str, encoding='utf-8')
    return engine

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_thread_exclusive_dbsession():
    if not hasattr(local, "db_session"):
        local.db_session = scoped_session(Session)
    return local.db_session

eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
db_session = get_thread_exclusive_dbsession()
metadata = MetaData(get_engine())

__all__ = ['eng', 'Base', 'db_session', 'metadata']
