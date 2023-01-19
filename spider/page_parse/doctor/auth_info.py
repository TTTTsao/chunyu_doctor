from spider.db.models import DoctorAuthInfo
from spider.util.reg.reg_doctor import get_reg_auth_time
from spider.util.reg.reg_hospital import (get_reg_hospital_id, get_reg_clinic_id)

from lxml import etree

def get_doctor_auth_info(doctor_id, html):
    '''
    从医生页面获取认证信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html: return

    xpath = etree.HTML(html)
    doctor_auth_info = DoctorAuthInfo()
    doctor_auth_info.doctor_id = doctor_id
    try:
        hospital_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[2]/a/@href")[0]
        clinic_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/a[1]/@href")[0]
        auth_grade = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[2]/text()")[0]
        auth_time = xpath.xpath("//div[@class='tip-inner']//div[@class='content-wrap']/div[3]/div[2]/text()")[0]
        auth_status = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[3]/text()")[0]
    # TODO 1.将该错误记录于日志 2.记录该doctor_id用于后续重新尝试爬取
    except IndexError: return

    doctor_auth_info.doctor_auth_hospital_id = get_reg_hospital_id(str(hospital_id))
    doctor_auth_info.doctor_auth_clinic_id = get_reg_clinic_id(str(clinic_id))
    doctor_auth_info.doctor_auth_grade = str(auth_grade)
    doctor_auth_info.doctor_auth_time = get_reg_auth_time(str(auth_time))

    if str(auth_status) == "已认证":
        doctor_auth_info.doctor_auth_status = 1
    else:
        doctor_auth_info.doctor_auth_status = 0

    return doctor_auth_info