from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.comment_label import get_doctor_comment_label

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
    # TODO crawl-info 正在抓取xx医生患者评价标签
    # crawler.info('the crawling url is {url}'.format(url=url))
    doctor_comment_label_data = get_doctor_comment_label(doctor_id, html)
    # 不存在
    if not doctor_comment_label_data:
        # TODO parse-waring 日志警告 不存在医生患者评价标签
        return

    if not DoctorCommentLabelOper.get_doctor_comment_label_by_doctor_id(doctor_id):
        # TODO storage-info 插入日志：新增
        DoctorCommentLabelOper.add_one(doctor_comment_label_data)
    else:
        # TODO storage-info 日志：已存在并更新
        DoctorCommentLabelOper.add_one(doctor_comment_label_data)
    # TODO storage-error 日志-插入失败