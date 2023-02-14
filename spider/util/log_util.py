import sys
from spider.config.conf import get_logger_logging_format
from loguru import logger
logging_format = get_logger_logging_format()

def create_crawl_logger():
    logger.add(sys.stderr, level="INFO", format=logging_format)
    logger.add('spider/logs/crawl_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/crawl_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/crawl_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    return logger

def create_parse_logger():
    logger.add(sys.stderr, level="INFO", format=logging_format)
    logger.add('spider/logs/parse_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/parse_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/parse_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    return logger

def create_storage_logger():
    logger.add(sys.stderr, level="INFO", format=logging_format)
    logger.add('spider/logs/storage_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/storage_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/storage_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    return logger

def create_other_logger():
    logger.add(sys.stderr, level="INFO", format=logging_format)
    logger.add('spider/logs/other_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/other_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    logger.add('spider/logs/other_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB",
               encoding='utf-8')
    return logger