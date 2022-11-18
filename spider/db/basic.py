import os

from sqlalchemy import (
    create_engine, MetaData)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from spider.config.conf import get_db_args


def get_engine():
    args = get_db_args()
    # print(type(args['password']))
    # print(args['password'])
    password = os.getenv('DB_PASS', '@#guest87654321@#')
    # print("password", password)
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(args['db_type'], args['user'], password,
                                                             args['host'], args['port'], args['db_name'])
    print(connect_str)
    engine = create_engine(connect_str, encoding='utf-8')
    return engine


eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
db_session = Session()
metadata = MetaData(get_engine())


__all__ = ['eng', 'Base', 'db_session', 'metadata']
