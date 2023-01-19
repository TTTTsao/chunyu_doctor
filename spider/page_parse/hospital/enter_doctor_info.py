from lxml import etree

from spider.util.reg.reg_hospital import get_reg_clinic_id
from spider.db.models import HospitalClinicEnterDoctor

def get_hospital_enter_doctor_info(hospital_id, html):
    '''
    get hospital enter doctor info from detail page
    :param hospital_id:
    :return: hospital_enter_doctor_info data
    '''
    if not html:
        return
    xpath = etree.HTML(html)
    hospital_enter_datas = []

    # 判断页面科室暂无的情况
    try:
        if '暂无相关信息' in html:
            # TODO parse-warning 暂无该科室信息日志记录
            print("暂无相关信息")
            return False
    except AttributeError:
        return False

    row_clinic_id_list = xpath.xpath('//*[@id="clinic"]/li/a/@href')
    row_enter_nums_list = xpath.xpath('//*[@id="clinic"]/li/span/i/text()')

    # 判断该科室是否为0人，如果是0人需要返回0
    for i in range(len(row_clinic_id_list)):
        hospital_enter_data = HospitalClinicEnterDoctor()
        hospital_enter_data.hospital_id = hospital_id
        hospital_enter_data.hospital_clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
        if len(row_clinic_id_list) > len(row_enter_nums_list):
            # 有科室为0人
            if ( i - len(row_enter_nums_list) ) > -1:
                # 为0人的科室
                hospital_enter_data.hospital_clinic_amount = 0
            else:
                hospital_enter_data.hospital_clinic_amount = int(row_enter_nums_list[i])
        else:
            hospital_enter_data.hospital_clinic_amount = int(row_enter_nums_list[i])

        hospital_enter_datas.append(hospital_enter_data)

    return hospital_enter_datas