from spider.db.models import DoctorAuthInfo
from spider.util.reg.reg_doctor import get_reg_auth_time
from spider.util.reg.reg_hospital import (get_reg_hospital_id, get_reg_clinic_id)
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import is_doctor_detail_page_right

from lxml import etree

import sys
from loguru import logger

from spider.config.conf import get_logger_logging_format
logging_format = get_logger_logging_format()

@parse_decorator(False)
def get_doctor_auth_info(doctor_id, html):
    '''
    从医生页面获取认证信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return False

    if not is_doctor_detail_page_right(doctor_id, html):
        logger.error("被反爬，{} 医生详情页面与医生不一致".format(doctor_id))
        # TODO 增加将未成功爬取的doctor_id 写入一个json文件 用于后续爬取
        return False
    xpath = etree.HTML(html)
    doctor_auth_info = DoctorAuthInfo()
    doctor_auth_info.doctor_id = doctor_id
    try:
        hospital_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[2]/a/@href")[0]
        clinic_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/a[1]/@href")[0]
        auth_grade = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[2]/text()")[0]
        auth_time = xpath.xpath("//div[@class='tip-inner']//div[@class='content-wrap']/div[3]/div[2]/text()")[0]
        auth_status = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[3]/text()")[0]
    except IndexError as e:
        logger.error("解析 {} 医生认证信息错误，详情：{}".format(doctor_id, e))
        return False

    doctor_auth_info.doctor_auth_hospital_id = get_reg_hospital_id(str(hospital_id))
    doctor_auth_info.doctor_auth_clinic_id = get_reg_clinic_id(str(clinic_id))
    doctor_auth_info.doctor_auth_grade = str(auth_grade)
    doctor_auth_info.doctor_auth_time = get_reg_auth_time(str(auth_time))

    if str(auth_status) == "已认证":
        doctor_auth_info.doctor_auth_status = 1
    else:
        doctor_auth_info.doctor_auth_status = 0

    if not doctor_auth_info:
        return False
    else:
        return doctor_auth_info