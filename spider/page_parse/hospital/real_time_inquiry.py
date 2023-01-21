from lxml import etree

from spider.db.models import HospitalRealTimeInquiry
from spider.decorators.parse_decorator import parse_decorator

@parse_decorator(False)
def get_hospital_real_time_inquiry(hospital_id, html):
    '''
    get hospital realtime inquiry doctors nums info from detail page
    :param hospital_id:
    :return: hospital_realtime_inquiry_nums data
    '''
    if not html:
        return
    hospital_real_time_inquiry_data = HospitalRealTimeInquiry()
    xpath = etree.HTML(html)

    hospital_real_time_inquiry_data.hospital_id = hospital_id
    try:
        inquiry_nums = xpath.xpath("//span[@class='light'][2]/text()")[0]
        hospital_real_time_inquiry_data.real_time_inquiry_doctor_num = int(inquiry_nums)
    except Exception:
        hospital_real_time_inquiry_data.real_time_inquiry_doctor_num = 0

    return hospital_real_time_inquiry_data