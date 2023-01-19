from lxml import etree

from spider.db.models import HospitalRealTimeInquiry

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

    # TODO 1.将该错误记录于日志 2.记录该hospital_id用于后续重新尝试爬取
    try:
        inquiry_nums = xpath.xpath("//span[@class='light'][2]/text()")[0]
        hospital_real_time_inquiry_data.real_time_inquiry_doctor_num = int(inquiry_nums)
    except:
        hospital_real_time_inquiry_data.real_time_inquiry_doctor_num = 0

    return hospital_real_time_inquiry_data