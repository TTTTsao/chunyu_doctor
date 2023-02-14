import time
import sys
from spider.config.conf import get_logger_logging_format
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from loguru import logger
from spider.decorators.crawl_decorator import timeout_decorator
from spider.page_parse.basic import is_404
from spider.config import headers
from spider.util.proxy.get_ip import getIP
from spider.config.conf import (get_timeout, get_crawl_interal, get_excp_interal, get_max_retries)
TIME_OUT = get_timeout()
INTERAL = get_crawl_interal()
MAX_RETRIES = get_max_retries()
EXCP_INTERAL = get_excp_interal()

# Disable annoying InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging_format = get_logger_logging_format()
logger.add(sys.stderr, level="INFO", format=logging_format)
logger.remove()
logger.add('spider/logs/crawl_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/crawl_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/crawl_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')

@timeout_decorator
def get_page_html(url):
    '''
    :param url:
    :return:
    获取网页的html文本
    :param url: url to crawl
    :return: responseonse text, when a exception is raised, return ''
    '''
    count = 0
    # 小于爬虫重试次数时
    while count < MAX_RETRIES:
        try :
            proxies = getIP()
            logger.info("第 {} 次爬取 url {}, 当前代理为 {}".format(count, url, proxies))
            response = requests.get(url, headers=headers, timeout=TIME_OUT, verify=False, proxies=proxies, stream=True)
            if response.status_code != 200:
                check_response(response, proxies)
        except(requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
            logger.warning("爬取 {} 时出现异常 {}".format(url, e))
            count += 1
            continue
        # 抓取文本内容
        try:
            if response.text:
                page = response.text.encode('utf-8', 'ignore').decode('utf-8')
                response.close()
            else:
                count += 1
                response.close()
                continue
        except Exception as e:
            logger.error("获取 {} 响应text 时出现异常 {}".format(url, e))
            response.close()
            return ''
         # 页面不存在
        if is_404(page):
            logger.warning("{} 为 404 页面".format(url))
            return ''
        return page
    logger.error("爬取 {} 时超过最大爬取次数".format(url))
    return ''

def check_response(response, proxies):
    '''
    处理response的错误
    :param response:
    :param proxies:
    :return:
    '''
    if response.status_code == 403:
        logger.warning("status_code:403, proxies:%s 没有权限" % proxies)
        raise Exception("status_code:403, proxies:%s 没有权限" % proxies)
    elif response.status_code == 414:
        logger.warning("status_code:414, proxies:%s 被封禁" % proxies)
        raise Exception("status_code:414, proxies:%s 被封禁" % proxies)
    elif response.status_code == 418:
        logger.warning("status_code:418, proxies:%s 被反爬" % proxies)
        time.sleep(EXCP_INTERAL)
        raise Exception("status_code:418, proxies:%s 被反爬" % proxies)
    elif response.status_code == 449:
        logger.warning("status_code:449, proxies:%s 被认为是海外IP" % proxies)
        raise Exception("status_code:449, proxies:%s 被认为是海外IP" % proxies)
    elif response.status_code == 429:
        logger.warning("status_code:429, proxies:%s 被认为请求频繁" % proxies)
        time.sleep(EXCP_INTERAL)
        raise Exception("status_code:429, proxies:%s 被认为请求频繁" % proxies)
