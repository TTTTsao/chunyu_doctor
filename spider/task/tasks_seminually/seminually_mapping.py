from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.description import get_doctor_description
from spider.page_parse.doctor.auth_info import get_doctor_auth_info
from spider.page_parse.doctor.tag import get_doctor_tag
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger
from spider.db.dao.doctor_dao import *
from spider.db.dao.hospital_dao import HospitalClinicRankOper
from spider.page_parse.hospital.hospital_clinic_rank import get_hospital_clinic_rank


HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def doctor_seminually_crawl(doctor_id):
    '''
    [每半年抓取-doctor低频更新信息]
    doctor_auth_info:认证信息
    doctor_description_info:个人简介
    doctor_tag:个人标签
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取医生 {} 低频更新更新信息".format(doctor_id))

    doctor_auth_data = get_doctor_auth_info(doctor_id, html)
    doctor_description_data = get_doctor_description(doctor_id, html)
    doctor_tag_data = get_doctor_tag(doctor_id, html)

    if not doctor_auth_data:
        logger.warning("{} 医生不存在认证信息".format(doctor_id))
        return
    if not DoctorAuthInfoOper.get_doctor_auth_info_by_doctor_id(doctor_id):
        # 表中未有认证信息
        DoctorAuthInfoOper.add_one(doctor_auth_data)
    else:
        # 表中存在认证信息-更新
        DoctorAuthInfoOper.update_auth_info_by_doctor_id(doctor_auth_data)

    if not doctor_description_data:
        logger.warning("{} 医生不存在个人简介信息".format(doctor_id))
        return
    if not DoctorDescriptionOper.get_doctor_description_by_doctor_id(doctor_id):
        # 表中未有医生个人简介信息
        DoctorDescriptionOper.add_one(doctor_description_data)
    else:
        # 表中存在医生个人简介信息-更新
        DoctorDescriptionOper.update_description_info_by_doctor_id(doctor_description_data)

    if not doctor_tag_data:
        logger.warning("{} 医生不存在个人标签信息".format(doctor_id))
        return
    if not DoctorTagOper.get_doctor_tag_by_doctor_id(doctor_id):
        DoctorTagOper.add_one(doctor_tag_data)
    else:
        DoctorTagOper.update_tag_by_doctor_id(doctor_tag_data)

@crawl_decorator
def hospital_seminually_crawl(hospital_id):
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    logger.info("正在抓取医院 {} 低频更新更新信息".format(hospital_id))
    pass