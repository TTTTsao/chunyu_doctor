from spider.db.models import DoctorBaseInfo
from spider.util.reg.reg_doctor import (get_reg_doctor_id, get_reg_doctor_name)

from lxml import etree

def get_active_doctor_base_info(html):
    '''
    get active doctor base info data
    从【根据科室找医生】获取活跃的医生基本信息
    :param html:
    :return:
    '''
    if not html:
        return

    xpath = etree.HTML(html)
    doctor_name_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/span[1]/text()")
    doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_base_info_datas = []

    for i in range(len(doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_name = get_reg_doctor_name(str(doctor_name_list[i]))

        doctor_base_info = DoctorBaseInfo()
        doctor_base_info.doctor_id = doctor_id
        doctor_base_info.doctor_name = doctor_name
        doctor_base_info_datas.append(doctor_base_info)

    return doctor_base_info_datas

def get_doctor_base_info(doctor_id, html):
    '''
    从医生个人主页页面获取基本信息
    :param html:
    :return: doctor base info 对象
    '''
    if not html:
        return

    doctor_base_info = DoctorBaseInfo()
    xpath = etree.HTML(html)

    doctor_base_info.doctor_id = doctor_id
    doctor_name = str(xpath.xpath('/html/body/div[4]/div[1]/div[1]/div/div[2]/div[1]/span[1]/text()')[0])
    doctor_base_info.doctor_name = doctor_name

    return doctor_base_info


def get_doctor_base_info_from_clinic(html):
    '''
    get doctor base info from clinic page
    从科室详情页获取医生基本信息
    :param html:
    :return:
    '''
    if not html:
        return
    xpath = etree.HTML(html)

    doctor_id_list = xpath.xpath("//div[@class='avatar-wrap']/a/@href")
    doctor_name_list = xpath.xpath("//div[@class='detail']/div/a/span[1]/text()")

    # 判断页面有无医生
    if len(doctor_id_list) == 0:
        # TODO parse-warning 日志-该科室没有医生
        print("该科室没有医生")
        return

    doctor_base_info_datas = []
    for i in range(len(doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_name = get_reg_doctor_name(str(doctor_name_list[i]))

        doctor_base_info = DoctorBaseInfo()
        doctor_base_info.doctor_id = doctor_id
        doctor_base_info.doctor_name = doctor_name
        doctor_base_info_datas.append(doctor_base_info)

    return doctor_base_info_datas