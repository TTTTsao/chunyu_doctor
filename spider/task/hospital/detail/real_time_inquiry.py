from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalRealTimeInquiryOper
from spider.page_parse.hospital.real_time_inquiry import get_hospital_real_time_inquiry
from loguru import logger
from spider.decorators.crawl_decorator import crawl_decorator

from spider.db.models import HospitalRealTimeInquiry

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

@crawl_decorator
def crawl_hospital_real_time_inquiry(hospital_id):
    '''
    根据hospital_id爬取医院医生当前在线可咨询信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    logger.info("抓取 {} 医院医生当前在线可咨询信息".format(hospital_id))

    hospital_real_time_inquiry_data = get_hospital_real_time_inquiry(hospital_id, html)
    # 不存在
    if not hospital_real_time_inquiry_data:
        logger.warning(" {} 医院无医生当前在线可咨询信息".format(hospital_id))
        data = HospitalRealTimeInquiry()
        data.hospital_id = hospital_id
        data.real_time_inquiry_doctor_num = 0
        HospitalRealTimeInquiryOper.add_one(data)
        return
    HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)