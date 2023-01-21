import sys
import os
from functools import wraps
from traceback import format_tb
from loguru import logger

from spider.config.conf import get_logger_logging_format
logging_format = get_logger_logging_format()

log_dir = os.path.dirname(os.path.dirname(__file__))+'/logs'

logger.add(sys.stderr, level="INFO", format=logging_format)
logger.remove()
logger.add('spider/logs/crawl_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/crawl_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/crawl_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')


def timeout_decorator(func):
    @wraps(func)
    def time_limit(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception as e:
            logger.error('获取 {url} 失败，详情:{e}, stack is {stack}'.format(url=args[0], e=e, stack=format_tb(e.__traceback__)[0]))
            return None
    return time_limit

def crawl_decorator(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception as e:
            logger.error("请求配置层错误，方法名：%s，参数：%s\t%s，错误信息：%s" % (
                str(func.__name__), str([*args]), str(**kargs), str(e)))
            return None
    return wrapper



if __name__ == '__main__':
    print(log_dir)