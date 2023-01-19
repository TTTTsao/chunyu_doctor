from spider.db.models import DoctorCommentLabel
from spider.util.reg.reg_doctor import get_reg_label_num

from lxml import etree

def get_doctor_comment_label(doctor_id, html):
    '''
    从医生页面获取医生患者评价标签（id、4个评价标签的数量）
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html: return
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
    # TODO 1.将该错误记录于日志 2.记录该doctor_id用于后续重新尝试爬取
    except IndexError: return

    return doctor_comment_label_data