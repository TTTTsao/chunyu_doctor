import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from spider.page_parse.basic import is_404
from spider.config import headers
# from spider.util.proxy import get_ip
from spider.logger import crawler
from spider.config.conf import (
    get_timeout, get_crawl_interal, get_excp_interal, get_max_retries)

TIME_OUT = get_timeout()
INTERAL = get_crawl_interal()
MAX_RETRIES = get_max_retries()
EXCP_INTERAL = get_excp_interal()

# Disable annoying InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Get Page HTML 获取网页的html文本
def get_page_html(url):
    '''
    :param url: url to crawl
    :return: response text, when a exception is raised, return ''
    '''

    count = 0
    # proxy = get_ip()
    # 小于爬虫重试次数时
    while count < MAX_RETRIES:
        try :
            resp = requests.get(url, headers=headers, timeout=TIME_OUT, verify=False)
        except(requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
            # 警告日志记录
            # crawler.warning('Excepitons are raised when crawling {}.Here are details:{}'.format(url, e))
            count += 1
            continue

        # 抓取文本内容
        if resp.text:
            page = resp.text.encode('utf-8', 'ignore').decode('utf-8')
        else:
            count += 1
            continue

        # TODO 用redis存储抓取到url，然后返回page

        #  404：url不存在
        if is_404(page):
            # crawler.warning('{} seems to be 404'.format(url))
            return ''

        # TODO 处理错误
        #  414：ip被封
        #  403：没有权限（账号被封）
        #  429: 过多请求
        #  需要login
        #  需要proxy
        #  需要login + cookie

        return page

    # 用redis存储抓取到url，然后返回null
    return ''

