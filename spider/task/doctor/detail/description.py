from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.description import get_doctor_description

from spider.db.dao.doctor_dao import DoctorDescriptionOper
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_description(doctor_id):
    '''
    抓取医生个人简介信息（id、教育背景、专业擅长、个人简介、医院地点）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生的个人简介信息".format(doctor_id))
    doctor_description_data = get_doctor_description(doctor_id, html)

    # 不存在
    if not doctor_description_data:
        logger.warning("无法获取 {} 医生的个人简介信息".format(doctor_id))
        return

    DoctorDescriptionOper.add_one(doctor_description_data)