import json
import threading

from spider.page_get.request_to_response import get
from spider.decorators.crawl_decorator import request_decorator
from spider.util.log_util import create_crawl_logger
logger = create_crawl_logger()
logger.remove()


DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'
DOCTOR_MOBILE_URL = 'https://m.chunyuyisheng.com/m/doctor/{}'
RECOMMEND_DOCTOR_URL = 'https://chunyuyisheng.com/pc/doctors/0-0-{}/?page={}'
RECOMMEND_AVAILABLE_DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctors/0-0-{}/?is_available=1&page={}'
INQUIRY_URL = 'https://www.chunyuyisheng.com/pc/qa/{}'
ILLNESS_BASE_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}/qa/?is_json=1&tag=&page_count=20&page=1'
ILLNESS_AJAX_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}/qa/?is_json=1&page_count=20&page={}&tag={}'
ILLNESS_AJAX_NO_TAG_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}/qa/?is_json=1&page_count=20&page={}'

@request_decorator
def get_doctor_moblie_detail_page(doctor_id):
    '''
    获取医生mobile详情页面（使用ip池+定制请求头）
    :param doctor_id: 医生id
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = DOCTOR_MOBILE_URL.format(doctor_id)
    logger.info(f"线程 {thread.getName()} 请求 doctor_id: {doctor_id} 移动端详情页 {url}")
    headers = {
        'authority': 'm.chunyuyisheng.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'connection': 'close',
    }
    response = get(url, False, True, headers=headers)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')


@request_decorator
def get_doctor_detail_page(doctor_id):
    '''
    获取医生pc详情页面（使用ip池+定制请求头）
    :param doctor_id: 医生id
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = DOCTOR_URL.format(doctor_id)
    logger.info(f"线程 {thread.getName()} 请求 doctor_id: {doctor_id} 详情页 {url}")
    headers = {
        'authority': 'www.chunyuyisheng.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'referer': 'https://chunyuyisheng.com/',
        'connection': 'close',
    }
    response = get(url, False, True, headers=headers)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')

@request_decorator
def get_doctor_illness_init_json(doctor_id):
    '''
    获取医生好评问题最初json页面（需要定制headers）
    :param doctor_id:
    :return: response.json()对象/None（错误）
    '''
    thread = threading.current_thread()
    url = ILLNESS_BASE_URL.format(doctor_id)
    logger.info(f"线程 {thread.getName()} 请求 doctor_id: {doctor_id} 好评问题初始json {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': f'https://www.chunyuyisheng.com/pc/doctor/{doctor_id}',
        'Connection': 'close',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = get(url, True, False, headers=headers)
    if response is None:
        return None
    return response

@request_decorator
def get_doctor_illness_json_with_page(doctor_id, cur_page, type_item):
    '''
    获取医生好评问题最初json页面（需要定制headers）
    :param doctor_id:
    :return: response.json()对象/None（错误）
    '''
    thread = threading.current_thread()
    if type_item == None:
        url = ILLNESS_AJAX_NO_TAG_URL.format(doctor_id, cur_page)
    else:
        url = ILLNESS_AJAX_URL.format(doctor_id, cur_page, type_item)
    logger.info(f"线程 {thread.getName()} 请求 doctor_id: {doctor_id} 好评问题 第 {cur_page} 页, 类型 {type_item}, json {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'close',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = get(url, True, False, headers=headers)
    if response is None:
        return None
    return response

@request_decorator
def get_doctor_topic_json(doctor_id):
    # TODO 获取医生分享文章json
    thread = threading.current_thread()


@request_decorator
def get_doctor_inquiry_detail_page(question_id):
    '''
    获取医生好评问题对话pc详情页面（使用ip池+定制请求头）
    :param question_id: 问题id
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = INQUIRY_URL.format(question_id)
    logger.info(f"线程 {thread.getName()} 请求医生问诊对话: {question_id} 信息")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'close',
    }
    response = get(url, False, True, headers=headers)
    if response is None:
        return None
    return response.text


@request_decorator
def get_recommend_doctor_page(clinic_id, page):
    '''
    获取【根据科室找医生】页面
    :param clinic_id: 科室id
    :param page: 页数（1-26）
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = RECOMMEND_DOCTOR_URL.format(clinic_id, page)
    logger.info(f"线程 {thread.getName()} 请求科室: {clinic_id} 第 {page} 页推荐医生信息")
    response = get(url, False, True)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')

@request_decorator
def get_recommend_available_doctor_page(clinic_id, page):
    '''
    获取【根据科室找医生】页面（仅可咨询）
    :param clinic_id: 科室id
    :param page: 页数（1-26）
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = RECOMMEND_AVAILABLE_DOCTOR_URL.format(clinic_id, page)
    logger.info(f"线程 {thread.getName()} 请求科室: {clinic_id} 第 {page} 页推荐医生信息")
    response = get(url, False, False)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')