import threading

from spider.util.log_util import create_crawl_logger
from spider.page_get.base_request import BaseRequest

logger = create_crawl_logger()
logger.remove()
local = threading.local()

def __get_base_request():
    '''
    获取当前线程唯一request对象
    :return: BaseRequest对象
    '''
    if not hasattr(local, "base_request"):
        local.base_request = BaseRequest()
    return local.base_request

def __check_response_status(response):
    '''
    检查response是否为None 且 检查response的状态码
    :param response:
    :return: True：为None或非200/201响应
    '''
    if response is None:
        return True
    elif response.status_code == 404:
        return False
    elif response.status_code != 200 and response.status_code != 201:
        return True
    return False

def __turn_response_to_html_or_json(response, is_response_json, url):
    '''
    将响应转换为相应格式（json/html）
    :param response: 响应对象
    :param is_response_json: 响应是否为json
    :param url: 抓取url
    :return: json对象/response对象/None（错误）
    '''
    if __check_response_status(response):
        logger.error("响应错误，url：%s，响应：%s" % (url, response))
        local.base_request.update_proxies()
        return None
    try:
        if is_response_json:
            json = response.json()
            return json
        else:
            return response
    except Exception as e:
        logger.error("响应转换失败，url：%s，错误信息：%s" % (url, e))

def get(url, is_response_json, is_enable_proxy, **kwargs):
    '''
    封装get请求
    :param url: 抓取url
    :param is_response_json: 响应是否为json
    :param is_enable_proxy: 是否需要代理ip
    :param kwargs: 其他参数
    :return: json对象/response对象/None（错误）
    '''
    response = __get_base_request().get(url, is_enable_proxy=is_enable_proxy, **kwargs)
    return __turn_response_to_html_or_json(response, is_response_json, url)