from spider.db.models import DoctorDescription
from spider.util.reg.reg_doctor import get_reg_doctor_profile
from spider.decorators.parse_decorator import parse_decorator
from lxml import etree

@parse_decorator(False)
def get_doctor_description(doctor_id, html):
    '''
    从医生页面获取个人简介信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    doctor_description_data = DoctorDescription()
    doctor_description_data.doctor_id = doctor_id

    xpath = etree.HTML(html)
    # 增加页面元素判断，是否存在某某字段-先判断是否有4个，有3个（无专业擅长）再做详细判断
    temp_length = len(xpath.xpath("//p[@class='detail']"))
    if temp_length == 4:
        edu_backgroud = xpath.xpath("//p[@class='detail']/text()")[1]
        doctor_description_data.doctor_description_edu_background = get_reg_doctor_profile(str(edu_backgroud))

        major = xpath.xpath("//p[@class='detail']/text()")[3]
        doctor_description_data.doctor_description_major = get_reg_doctor_profile(str(major))

        description = xpath.xpath("//p[@class='detail']/text()")[5]
        doctor_description_data.doctor_description_description = get_reg_doctor_profile(str(description))

        hospital_location = xpath.xpath("//p[@class='detail']/text()")[7]
        doctor_description_data.doctor_description_hospital_location = get_reg_doctor_profile(str(hospital_location))
    elif temp_length == 3:
        edu_backgroud = xpath.xpath("///p[@class='detail']/text()")[1]
        doctor_description_data.doctor_description_edu_background = get_reg_doctor_profile(str(edu_backgroud))

        description = xpath.xpath("//p[@class='detail']/text()")[3]
        doctor_description_data.doctor_description_description = get_reg_doctor_profile(str(description))

        hospital_location = xpath.xpath("//p[@class='detail']/text()")[5]
        doctor_description_data.doctor_description_hospital_location = get_reg_doctor_profile(str(hospital_location))

    return doctor_description_data