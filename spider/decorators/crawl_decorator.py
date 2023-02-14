from functools import wraps
from traceback import format_tb
from spider.util.log_util import create_crawl_logger
from sqlalchemy.exc import PendingRollbackError
logger = create_crawl_logger()
logger.remove()


def timeout_decorator(func):
    @wraps(func)
    def time_limit(*args, **kargs):
        try:
            logger.info("方法%s完成，参数：%s\t%s" % (str(func.__name__), str([*args]), str(**kargs)))
            return func(*args, **kargs)
        except Exception as e:
            logger.error('获取 {url} 失败，详情:{e}, stack is {stack}'.format(url=args[0], e=e, stack=format_tb(e.__traceback__)[0]))
            return ''
    return time_limit

def request_decorator(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        try:
            return func(*args, **kargs)
        except Exception as e:
            logger.error("请求配置层错误，方法名：%s，参数：%s\t%s，错误信息：%s" % (
                str(func.__name__), str([*args]), str(**kargs), str(e)))
            return None
    return wrapper

def crawl_decorator(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        try:
            result = func(*args, **kargs)
            logger.info("方法%s完成爬取，参数：%s\t%s" % (str(func.__name__), str([*args]), str(**kargs)))
            return result
        except Exception as e:
            if not isinstance(e, PendingRollbackError):
                logger.error("爬取失败：字段映射层错误，方法名：%s，参数：%s\t%s，错误信息：%s" % (str(func.__name__), str([*args]), str(**kargs), str(e)))
            return
    return wrapper

