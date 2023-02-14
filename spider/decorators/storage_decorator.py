import sys
from functools import wraps
from spider.db.basic import db_session

from spider.util.log_util import create_storage_logger
logger = create_storage_logger()
logger.remove()

def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            logger.info("数据插入 {} 表成功".format(args[0]))
            return func(*args, **kwargs)
        except Exception as e:
            logger.error('数据插入 {} 表失败，详情错误:{}'.format(args[0], e))
            db_session.rollback()
    return session_commit