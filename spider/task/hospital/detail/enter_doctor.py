from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalClinicEnterDoctorOper
from spider.page_parse.hospital.enter_doctor_info import get_hospital_enter_doctor_info
from loguru import logger
from spider.decorators.crawl_decorator import crawl_decorator

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

@crawl_decorator
def crawl_hospital_clinic_enter_doctor(hospital_id):
    '''
    根据hospital_id爬取医院医生入驻信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医院医生入驻信息".format(hospital_id))


    hospital_enter_data = get_hospital_enter_doctor_info(hospital_id, html)
    # 不存在
    if not hospital_enter_data:
        logger.warning("{} 医院不存在入驻医生信息".format(hospital_id))
        return

    HospitalClinicEnterDoctorOper.add_all(hospital_enter_data)