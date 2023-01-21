import sys
from functools import wraps
from spider.db.basic import db_session

from spider.config.conf import get_logger_logging_format
logging_format = get_logger_logging_format()

from loguru import logger
logger.add(sys.stderr, level="INFO", format=logging_format)
logger.remove()
logger.add('spider/logs/storage_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/storage_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/storage_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')


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