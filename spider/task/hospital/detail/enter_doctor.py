from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalClinicEnterDoctorOper
from spider.page_parse.hospital.enter_doctor_info import get_hospital_enter_doctor_info

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

def crawl_hospital_clinic_enter_doctor(hospital_id):
    '''
    根据hospital_id爬取医院医生入驻信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_enter_data = get_hospital_enter_doctor_info(hospital_id, html)
    # 不存在
    if not hospital_enter_data:
        # TODO 日志警告
        return

    # 不存在于表
    if not HospitalClinicEnterDoctorOper.get_hosital_clinic_enter_doctor_by_hospital_id(hospital_id):
        # TODO 插入日志：新增
        HospitalClinicEnterDoctorOper.add_all(hospital_enter_data)
    else:
        # TODO 日志：已存在并更新
        HospitalClinicEnterDoctorOper.add_all(hospital_enter_data)