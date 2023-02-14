from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.auth_info import *

from spider.db.dao.doctor_dao import DoctorAuthInfoOper
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_auth_info(doctor_id):
    '''
    crawl doctor auth info：抓取医生认证信息
    :param doctor_id:
    :return: doctor auth info 对象
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生的认证信息".format(doctor_id))
    doctor_auth_data = get_doctor_auth_info(doctor_id, html)

    if not doctor_auth_data:
        logger.warning("无法获取 {} 医生的认证信息".format(doctor_id))
        return

    if not DoctorAuthInfoOper.get_doctor_auth_info_by_doctor_id(doctor_id):
        # 表中未有认证信息
        DoctorAuthInfoOper.add_one(doctor_auth_data)
    else:
        # 表中存在认证信息-更新
        DoctorAuthInfoOper.update_auth_info_by_doctor_id(doctor_auth_data)