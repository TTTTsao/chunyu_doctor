from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.tag import *
from spider.db.dao.doctor_dao import DoctorTagOper
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_tag(doctor_id):
    '''
    抓取医生标签信息（id、tag【JSON形式存储】）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生的标签信息".format(doctor_id))
    doctor_tag_data = get_doctor_tag(doctor_id, html)
    # 不存在
    if not doctor_tag_data:
        logger.warning("{} 医生不存在标签信息".format(doctor_id))
        return

    if not DoctorTagOper.get_doctor_tag_by_doctor_id(doctor_id):
        DoctorTagOper.add_one(doctor_tag_data)
    else:
        DoctorTagOper.add_one(doctor_tag_data)