from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.price import *
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

from spider.db.dao.doctor_dao import DoctorPriceOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_price(doctor_id):
    '''
    抓取医生价格信息（id、价格、折扣【需判断有无】、类型）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生的价格信息".format(doctor_id))
    doctor_price_data = get_doctor_price(doctor_id, html)

    # 不存在
    if not doctor_price_data:
        logger.warning("{} 医生不存在价格信息".format(doctor_id))
        return

    DoctorPriceOper.add_one(doctor_price_data)

