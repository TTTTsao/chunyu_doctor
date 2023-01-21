from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.comment_label import get_doctor_comment_label

from spider.db.dao.doctor_dao import DoctorCommentLabelOper
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_comment_label(doctor_id):
    '''
    抓取医生患者评价标签（id、4个评价标签的数量）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生的患者评价标签".format(doctor_id))
    doctor_comment_label_data = get_doctor_comment_label(doctor_id, html)
    # 不存在
    if not doctor_comment_label_data:
        logger.warning("无法获取 {} 医生的患者评价标签".format(doctor_id))
        return

    DoctorCommentLabelOper.add_one(doctor_comment_label_data)