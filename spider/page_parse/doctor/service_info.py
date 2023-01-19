from decimal import Decimal

from spider.db.models import DoctorServiceInfo
from spider.util.reg.reg_doctor import get_reg_followers

from lxml import etree

def get_doctor_service_info(doctor_id, html):
    '''
    从医生页面获取服务信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html: return
    doctor_service_data = DoctorServiceInfo()
    doctor_service_data.doctor_id = doctor_id
    xpath = etree.HTML(html)

    try:
        serve_nums = xpath.xpath("//ul[@class='doctor-data']/li[1]/span[1]/text()")[0]
        favorable_rate = xpath.xpath("//ul[@class='doctor-data']/li[2]/span[1]/text()")[0]
        peer_recognization = xpath.xpath("//ul[@class='doctor-data']/li[3]/span[1]/text()")[0]
        patient_praise_num = xpath.xpath("//ul[@class='doctor-data']/li[4]/span[1]/text()")[0]
        followers = xpath.xpath("//div[@class='wexin-qr-code']//div[@class='footer-des']/text()")[0]
    # TODO 1.将该错误记录于日志 2.记录该doctor_id用于后续重新尝试爬取
    except IndexError: return

    doctor_service_data.doctor_serve_followers = get_reg_followers(str(followers))

    # 判断各值是否为'--'
    if str(serve_nums) == '--': doctor_service_data.doctor_serve_nums = 0
    else: doctor_service_data.doctor_serve_nums = int(serve_nums)

    if str(favorable_rate) == '--': doctor_service_data.doctor_serve_favorable_rate = 0
    else: doctor_service_data.doctor_serve_favorable_rate = Decimal(favorable_rate)

    if str(peer_recognization) == '--': doctor_service_data.doctor_serve_peer_recognization = 0
    else: doctor_service_data.doctor_serve_peer_recognization = Decimal(peer_recognization)

    if str(patient_praise_num) == '--': doctor_service_data.doctor_serve_patient_praise_num = 0
    else: doctor_service_data.doctor_serve_patient_praise_num = int(patient_praise_num)

    return doctor_service_data