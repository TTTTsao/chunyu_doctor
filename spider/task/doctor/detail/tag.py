from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.tag import *
from spider.db.dao.doctor_dao import DoctorTagOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_tag(doctor_id):
    '''
    抓取医生标签信息（id、tag【JSON形式存储】）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_tag_data = get_doctor_tag(doctor_id, html)
    # 不存在
    if not doctor_tag_data:
        # TODO 日志警告
        return

    if not DoctorTagOper.get_doctor_tag_by_doctor_id(doctor_id):
        # TODO  插入日志：新增
        DoctorTagOper.add_one(doctor_tag_data)
    else:
        # TODO 日志：已存在并更新
        DoctorTagOper.add_one(doctor_tag_data)