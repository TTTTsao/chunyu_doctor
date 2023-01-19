import json

from spider.db.models import DoctorTag

from lxml import etree

def get_doctor_tag(doctor_id, html):
    '''
    从医生页面获取标签信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html: return
    doctor_tag = DoctorTag()
    xpath = etree.HTML(html)

    doctor_tag.doctor_id = doctor_id
    tag_content_dict = {}
    label_list = xpath.xpath("/html/body/div[4]/div[1]/div[1]/div/div[2]/div[3]/span/text()")
    # 判断有几个标签
    for i in range(len(label_list)):
        label_name = 'label'+str(i+1)
        tag_content_dict[label_name] = label_list[i]

    tag_content_json = json.dumps(tag_content_dict, ensure_ascii=False)
    doctor_tag.tag_content = tag_content_json
    return doctor_tag