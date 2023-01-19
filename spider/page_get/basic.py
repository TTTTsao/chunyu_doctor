import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from spider.page_parse.basic import is_404
from spider.config import headers
from spider.util.proxy.get_ip import getIP
from spider.config.conf import (
    get_timeout, get_crawl_interal, get_excp_interal, get_max_retries)

TIME_OUT = get_timeout()
INTERAL = get_crawl_interal()
MAX_RETRIES = get_max_retries()
EXCP_INTERAL = get_excp_interal()

# Disable annoying InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_page_html(url):
    '''
    获取网页的html文本
    :param url: url to crawl
    :return: responseonse text, when a exception is raised, return ''
    '''

    count = 0
    proxies = getIP()
    # 小于爬虫重试次数时
    while count < MAX_RETRIES:
        try :
            # TODO 记录当前爬取次数：info
            response = requests.get(url, headers=headers, timeout=TIME_OUT, verify=False, proxies=proxies)
            if response != 200: check_response(response, proxies)
        except(requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
            # TODO 警告日志记录：warning
            # crawler.warning('Excepitons are raised when crawling {}.Here are details:{}'.format(url, e))
            count += 1
            continue

        # 抓取文本内容
        if response.text:
            page = response.text.encode('utf-8', 'ignore').decode('utf-8')
        else:
            count += 1
            continue
        #  页面不存在
        if is_404(page):
            # TODO 警告日志记录：warning
            # crawler.warning('{} seems to be 404'.format(url))
            return ''

        return page
    # TODO 错误日志记录：error-完成最大爬取尝试次数仍失败

    return ''

def check_response(response, proxies):
    '''
    处理response的错误
    :param response:
    :param proxies:
    :return:
    '''
    if response.status_code == 403:
        raise Exception("status_code:403, proxies:%s 没有权限" % proxies)
    elif response.status_code == 414:
        raise Exception("status_code:414, proxies:%s 被封禁" % proxies)
    elif response.status_code == 418:
        # TODO 警告日志
        time.sleep(EXCP_INTERAL)
        raise Exception("status_code:418, proxies:%s 被反爬" % proxies)
    elif response.status_code == 449:
        raise Exception("status_code:449, proxies:%s 被认为是海外IP" % proxies)
    elif response.status_code == 429:
        time.sleep(EXCP_INTERAL)
        raise Exception("status_code:429, proxies:%s 被认为请求频繁" % proxies)



if __name__ == '__main__':
    url = "https://www.chunyuyisheng.com/pc/doctor/1f550cdb982f90787117/"
    get_page_html(url)