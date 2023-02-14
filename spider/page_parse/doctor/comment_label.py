from spider.db.models import DoctorCommentLabel
from spider.util.reg.reg_doctor import get_reg_label_num
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import is_doctor_detail_page_right

from lxml import etree

import sys
from loguru import logger

from spider.config.conf import get_logger_logging_format
logging_format = get_logger_logging_format()

logger.add(sys.stderr, level="INFO", format=logging_format)
logger.add('spider/logs/parse_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/parse_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/parse_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')

@parse_decorator(False)
def get_doctor_comment_label(doctor_id, html):
    '''
    从医生页面获取医生患者评价标签（id、4个评价标签的数量）
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    if not is_doctor_detail_page_right(doctor_id, html):
        logger.error("被反爬，{} 医生详情页面与医生不一致".format(doctor_id))
        return False
    doctor_comment_label_data = DoctorCommentLabel()
    doctor_comment_label_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    label_num_list = xpath.xpath("//ul[@class='tags']/li/span/text()")

    try:
        # 判断是否存在【患者评价】板块
        if len(label_num_list) == 0:
            doctor_comment_label_data.doctor_comment_attitude = 0
            doctor_comment_label_data.doctor_comment_explanation = 0
            doctor_comment_label_data.doctor_comment_reply = 0
            doctor_comment_label_data.doctor_comment_suggestion = 0
        else:
            doctor_comment_label_data.doctor_comment_attitude = get_reg_label_num(str(label_num_list[0]))
            doctor_comment_label_data.doctor_comment_explanation = get_reg_label_num(str(label_num_list[1]))
            doctor_comment_label_data.doctor_comment_reply = get_reg_label_num(str(label_num_list[2]))
            doctor_comment_label_data.doctor_comment_suggestion = get_reg_label_num(str(label_num_list[3]))
    except IndexError:
        logger.error("获取 {} 医生患者评价标签失败".format(doctor_id))
        return False

    return doctor_comment_label_data