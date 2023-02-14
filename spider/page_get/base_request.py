import time
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from spider.util.log_util import create_crawl_logger
from spider.config.conf import (get_timeout, get_crawl_interal, get_max_retries, get_excp_interal, get_choose_proxy)
from spider.util.proxy.get_ip import getIP
from spider.util.proxy.zm_proxy import __fetch_proxy
from spider.config import headers
_headers = headers
logger = create_crawl_logger()
logger.remove()

TIME_OUT = get_timeout()
INTERAL = get_crawl_interal()
MAX_RETRIES = get_max_retries()
EXCP_INTERAL = get_excp_interal()

# Disable annoying InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_proxies():
    """
    选择使用的IP池
    :return:
    """
    if get_choose_proxy() == 'zm':
        return __fetch_proxy()
    else:
        return getIP()


class BaseRequest:

    def __init__(self):
        self.proxies = {}
        self.update_proxies()

    def update_proxies(self):
        self.proxies = get_proxies()

    def check_response(self, response):
        status_code = response.status_code
        if status_code == 418:
            logger.warning("反爬检测, 暂停 %d 秒" % (5 * 60))
            time.sleep(EXCP_INTERAL)
            raise Exception(f"status_code: 418, 反爬, proxy: {self.proxies}")
        elif status_code == 429:
            logger.warning("status_code:429, proxies:%s 被认为请求频繁" % (self.proxies))
            time.sleep(EXCP_INTERAL)
            time.sleep(random.randrange(5, 10))
            raise Exception(f"status_code: 429, 请求频繁, proxy: {self.proxies}")
        elif status_code == 404:
            logger.warning("status_code:404, 响应页面不存在")
            return response
        if not 200 <= status_code < 300:
            raise Exception(f"status_code: {status_code}, 其他错误")

    def get(self, url, headers=None, is_enable_proxy=False, **kwargs):
        if headers is None:
            headers = _headers
        else:
            headers.update(_headers)

        for i in range(MAX_RETRIES):
            logger.debug("第 {} 次 抓取 url: {}".format(i+1, url))
            if is_enable_proxy:
                try:
                    response = requests.get(url, headers=headers, proxies=self.proxies, timeout=get_timeout(), verify=False, **kwargs)
                    self.check_response(response)
                    return response
                except Exception as e:
                    logger.warning("第 {} 次使用proxy : {} 抓取失败，错误详情：{}".format(i+1, self.proxies, e))
                    self.update_proxies()
            else:
                try:
                    response = requests.get(url, headers=headers, timeout=get_timeout(),verify=False, **kwargs)
                    self.check_response(response)
                    return response
                except Exception as e:
                    logger.warning("第 {} 次不使用proxy抓取失败，错误详情：{}".format(i+1, e))
            time.sleep(random.uniform(1, 3))
        logger.error("请求错误，重试次数已用完，url：%s" % url)
        time.sleep(random.uniform(TIME_OUT, TIME_OUT * MAX_RETRIES))
