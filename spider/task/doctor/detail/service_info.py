from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.service_info import *

from spider.db.dao.doctor_dao import *

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_service_info(doctor_id):
    '''
    抓取医生服务信息（id、服务人次、好评率、同行认可、患者心意、关注人数）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    # TODO crawl-info 正在抓取xx医生服务信息
    # crawler.info('the crawling url is {url}'.format(url=url))
    doctor_service_data = get_doctor_service_info(doctor_id, html)

    # 不存在
    if not doctor_service_data:
        # TODO parse-waring 日志警告 不存在服务信息
        return

    if not DoctorServiceInfoOper.get_doctor_service_info_by_doctor_id(doctor_id):
        # TODO storage-info 插入日志：新增
        print("插入doctor_service_data")
        DoctorServiceInfoOper.add_one(doctor_service_data)
    else:
        # TODO storage-info 日志：已存在并更新
        DoctorServiceInfoOper.add_one(doctor_service_data)
    # TODO storage-error 日志-插入失败

