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
logger.add('spider/logs/parse_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/parse_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/parse_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')

def parse_decorator(return_value):
    def page_parse(func):
        @wraps(func)
        def handle_error(*keys):
            try:
                return func(*keys)
            except Exception as e:
                logger.error("解析页面失败，出现 {} 错误，详情：{}".format(e, format_tb(e.__traceback__)[0]))
                return return_value
        return handle_error
    return page_parse