from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.price import get_doctor_price
from spider.page_parse.doctor.service_info import get_doctor_service_info
from spider.page_parse.doctor.comment_label import get_doctor_comment_label
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger
from spider.db.dao.doctor_dao import *
DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def daily_crawl(doctor_id):
    '''
    [每日抓取-doctor高频更新信息]
    doctor_price:价格信息
    doctor_service_info:服务信息
    doctor_comment_label:评价标签数量
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生高频更新信息".format(doctor_id))

    doctor_price_data = get_doctor_price(doctor_id, html)
    doctor_service_data = get_doctor_service_info(doctor_id, html)
    doctor_comment_label = get_doctor_comment_label(doctor_id, html)

    if not doctor_price_data:
        logger.warning("{} 医生不存在价格信息".format(doctor_id))
        return
    DoctorPriceOper.add_one(doctor_price_data)

    if not doctor_service_data:
        logger.warning("{} 医生不存在服务信息".format(doctor_id))
        return
    DoctorServiceInfoOper.add_one(doctor_service_data)

    if not doctor_comment_label:
        logger.warning("{} 医生不存在服务信息".format(doctor_id))
        return
    DoctorCommentLabelOper.add_one(doctor_comment_label)