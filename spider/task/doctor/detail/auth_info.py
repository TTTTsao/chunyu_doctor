from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.auth_info import *

from spider.db.dao.doctor_dao import DoctorAuthInfoOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_auth_info(doctor_id):
    '''
    crawl doctor auth info：抓取医生认证信息
    :param doctor_id:
    :return: doctor auth info 对象
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    # TODO crawl-info 正在抓取xx医生认证信息
    # crawler.info('the crawling url is {url}'.format(url=url))
    doctor_auth_data = get_doctor_auth_info(doctor_id, html)

    if not doctor_auth_data:
        # TODO parse-waring 日志警告-不存在这个认证信息
        return

    if not DoctorAuthInfoOper.get_doctor_auth_info_by_doctor_id(doctor_id):
        # TODO storage-info 插入日志：新增
        DoctorAuthInfoOper.add_one(doctor_auth_data)
    else:
        # TODO storage-info 日志：已存在并更新
        DoctorAuthInfoOper.add_one(doctor_auth_data)
    # TODO storage-error 日志-插入失败