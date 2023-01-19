from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.description import get_doctor_description

from spider.logger import crawler, storage
from spider.db.dao.doctor_dao import DoctorDescriptionOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_description(doctor_id):
    '''
    抓取医生个人简介信息（id、教育背景、专业擅长、个人简介、医院地点）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_description_data = get_doctor_description(doctor_id, html)

    # 不存在
    if not doctor_description_data:
        # TODO 日志警告
        return

    if not DoctorDescriptionOper.get_doctor_description_by_doctor_id(doctor_id):
        # TODO 插入日志：新增
        DoctorDescriptionOper.add_one(doctor_description_data)
    else:
        # TODO 日志：已存在并更新
        DoctorDescriptionOper.add_one(doctor_description_data)