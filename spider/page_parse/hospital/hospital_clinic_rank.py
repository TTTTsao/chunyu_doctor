from lxml import etree

from spider.util.reg.reg_hospital import (get_reg_rank_name, get_reg_rank_level)
from spider.db.models import HospitalClinicRank
from spider.decorators.parse_decorator import parse_decorator

@parse_decorator(False)
def get_hospital_clinic_rank(hospital_id, html):
    '''
    get clinic rank info from hospital detail page
    :param hospital_id:
    :return: clinic rank info data
    '''
    if not html:
        return False
    xpath = etree.HTML(html)
    hospital_clinic_rank_datas = []
    try:
        row_rank_data_list = xpath.xpath("//li[@class='hospital-rank']/a/text()")
    except Exception:
        return False

    # 判断是否存在排名信息
    if len(row_rank_data_list) == 0:
        return

    for i in range(len(row_rank_data_list)):
        hospital_clinic_rank = HospitalClinicRank()
        hospital_clinic_rank.hospital_id = hospital_id
        hospital_clinic_rank.rank_name = get_reg_rank_name(str(row_rank_data_list[i]))
        hospital_clinic_rank.rank_level = get_reg_rank_level(str(row_rank_data_list[i]))
        hospital_clinic_rank_datas.append(hospital_clinic_rank)

    return hospital_clinic_rank_datas