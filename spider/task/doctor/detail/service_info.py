from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.service_info import *
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger
from spider.db.dao.doctor_dao import *

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_service_info(doctor_id):
    '''
    抓取医生服务信息（id、服务人次、好评率、同行认可、患者心意、关注人数）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生服务信息".format(doctor_id))

    doctor_service_data = get_doctor_service_info(doctor_id, html)

    # 不存在
    if not doctor_service_data:
        logger.warning("{} 医生不存在服务信息".format(doctor_id))
        return

    DoctorServiceInfoOper.add_one(doctor_service_data)

