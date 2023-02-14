import json

from spider.db.models import DoctorTag
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import is_doctor_detail_page_right
from loguru import logger
from lxml import etree

@parse_decorator(False)
def get_doctor_tag(doctor_id, html):
    '''
    从医生页面获取标签信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    if not is_doctor_detail_page_right(doctor_id, html):
        logger.error("被反爬，{} 医生详情页面与医生不一致".format(doctor_id))
        # TODO 增加将未成功爬取的doctor_id 写入一个json文件 用于后续爬取
        return False
    doctor_tag = DoctorTag()
    xpath = etree.HTML(html)

    doctor_tag.doctor_id = doctor_id
    try:
        tag_content_dict = {}
        label_list = xpath.xpath("//div[@class='doctor-hospital']/span/text()")
    except Exception:
        return False

    # 判断有几个标签
    for i in range(len(label_list)):
        label_name = 'label'+str(i+1)
        tag_content_dict[label_name] = label_list[i]

    tag_content_json = json.dumps(tag_content_dict, ensure_ascii=False)
    doctor_tag.tag_content = tag_content_json
    return doctor_tag