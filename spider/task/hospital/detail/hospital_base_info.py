from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalOper
from spider.page_parse.hospital.hospital_base_info import get_hospital_base_info
from loguru import logger
from spider.decorators.crawl_decorator import crawl_decorator

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

@crawl_decorator
def crawl_hospital_base_info(hospital_id, city):
    '''
    根据hospital_id爬取医院基本信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    logger.info("开始抓取 {} 医院基本信息".format(hospital_id))

    hospital_base_data = get_hospital_base_info(hospital_id, city, html)
    # 不存在
    if not hospital_base_data:
        logger.warning("无法获取 {} 医院的基本信息".format(hospital_id))
        return

    # 不存在于表
    HospitalOper.add_one(hospital_base_data)