from spider.page_get.basic import get_page_html
from spider.page_parse.basic import is_404
from spider.db.dao.hospital_dao import HospitalClinicBaseInfoOper
from spider.page_parse.hospital.hospital_clinic_base_info import get_hospital_clinic_base_info
from loguru import logger
from spider.decorators.crawl_decorator import crawl_decorator

HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'

@crawl_decorator
def crawl_hospital_clinic_base_info(clinic_id):
    '''
    根据clinic_id爬取医院科室基本信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_CLINIC_URL.format(clinic_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 科室基本信息".format(clinic_id))

    try:
        if '暂无相关信息' in html:
            logger.warning("{} 科室页面暂无相关信息".format(clinic_id))
            return
        elif is_404(html):
            return
    except AttributeError:
        return False

    hospital_clinic_base_info = get_hospital_clinic_base_info(clinic_id, html)

    if not hospital_clinic_base_info:
        return
    # 不存在于表
    if not HospitalClinicBaseInfoOper.get_hospital_clinic_base_info_by_clinic_id(clinic_id):
        HospitalClinicBaseInfoOper.add_one(hospital_clinic_base_info)
    else:
        HospitalClinicBaseInfoOper.add_one(hospital_clinic_base_info)