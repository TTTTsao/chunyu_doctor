from lxml import etree

from spider.util.reg.reg_hospital import get_reg_clinic_profile
from spider.db.models import HospitalClinicBaseInfo
from spider.decorators.parse_decorator import parse_decorator

@parse_decorator(False)
def get_hospital_clinic_base_info(clinic_id, html):
    '''
    get hospital's clinic base info from clinic detail page
    :param clinic_id:
    :return: hospital_clinic_base_info data
    '''
    if not html:
        return False
    xpath = etree.HTML(html)
    hospital_clinic_data = HospitalClinicBaseInfo()

    hospital_clinic_data.hospital_clinic_id = clinic_id
    try:
        hospital_clinic_data.hospital_clinic_name = str(xpath.xpath("//h3[@class='title']//text()")[0])
    except IndexError:
        return False
    except Exception:
        return False

    row_profile = xpath.xpath('/html/body/div[4]/div[3]/div/p/text()')
    # 没有科室简介
    if len(row_profile) != 0:
        hospital_clinic_data.hospital_clinic_profile = get_reg_clinic_profile(str(row_profile))

    return hospital_clinic_data