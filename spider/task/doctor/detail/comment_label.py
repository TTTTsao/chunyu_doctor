from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.comment_label import get_doctor_comment_label

from spider.logger import crawler, storage
from spider.db.dao.doctor_dao import DoctorCommentLabelOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_comment_label(doctor_id):
    '''
    抓取医生患者评价标签（id、4个评价标签的数量）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_comment_label_data = get_doctor_comment_label(doctor_id, html)
    # 不存在
    if not doctor_comment_label_data:
        # TODO 日志警告
        return

    if not DoctorCommentLabelOper.get_doctor_comment_label_by_doctor_id(doctor_id):
        # TODO 插入日志：新增
        DoctorCommentLabelOper.add_one(doctor_comment_label_data)
    else:
        # TODO 日志：已存在并更新
        DoctorCommentLabelOper.add_one(doctor_comment_label_data)