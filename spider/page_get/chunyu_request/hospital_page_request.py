
import threading

from spider.page_get.request_to_response import get
from spider.decorators.crawl_decorator import request_decorator
from spider.util.log_util import create_crawl_logger
logger = create_crawl_logger()
logger.remove()

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_CLINIC_PAGE_URL = 'https://chunyuyisheng.com/pc/clinic/{}/?page={}'
HOSPITAL_RANK_URL = 'https://www.chunyuyisheng.com/pc/hospitallist/{}/{}'

@request_decorator
def get_hospital_deatil_page(hospital_id):
    '''
    获取医院详情页面（使用定制请求头，不使用ip池）
    :param hospital_id: 医院id
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    logger.info(f"线程 {thread.getName()} 请求 hospital_id: {hospital_id} 详情页 {url}")
    headers = {
        'authority': 'www.chunyuyisheng.com',
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
    response = get(url, False, False, headers=headers)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')

@request_decorator
def get_hospital_clinic_detail_page(hospital_clinic_id):
    '''
    获取医院科室详情页面
    :param hospital_clinic_id: 医院科室id
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = HOSPITAL_DETAIL_URL.format(hospital_clinic_id)
    logger.info(f"线程 {thread.getName()} 请求 hospital_clinic_id: {hospital_clinic_id} 详情页 {url}")
    response = get(url, False, False)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')

@request_decorator
def get_hospital_rank_page(area_id, clinic_id):
    '''
    获取医院排名页面
    :param area_id: 地区id
    :param clinic_id: 科室id
    :return: response.text对象/None（出错）
    '''
    thread = threading.current_thread()
    url = HOSPITAL_RANK_URL.format(area_id, clinic_id)
    logger.info(f"线程 {thread.getName()} 请求 area_id: {area_id} clinic_id: {clinic_id} rank {url}")
    response = get(url, False, False)
    if response is None:
        return None
    return response.text.encode('utf-8', 'ignore').decode('utf-8')
