import sys
import os
from functools import wraps
from traceback import format_tb
from spider.util.log_util import create_parse_logger
logger = create_parse_logger()
logger.remove()

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