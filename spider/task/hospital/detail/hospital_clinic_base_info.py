from spider.page_get.basic import get_page_html
from spider.page_parse.basic import is_404
from spider.db.dao.hospital_dao import HospitalClinicBaseInfoOper
from spider.page_parse.hospital.hospital_clinic_base_info import get_hospital_clinic_base_info

HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'

def crawl_hospital_clinic_base_info(clinic_id):
    '''
    根据clinic_id爬取医院科室基本信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_CLINIC_URL.format(clinic_id)
    html = get_page_html(url)
    # TODO crawl-info 正在抓取xx科室基本信息
    # crawler.info('the crawling url is {url}'.format(url=url))

    try:
        if '暂无相关信息' in html:
            # TODO crawl-warning 日志记录 页面科室暂无
            print("暂无相关信息")
            return
        elif is_404(html):
            return
    except AttributeError:
        return False

    hospital_clinic_base_info = get_hospital_clinic_base_info(clinic_id, html)

    if not hospital_clinic_base_info:
        # TODO parse-warning 日志警告 不存在该科室信息
        return
    # 不存在于表
    if not HospitalClinicBaseInfoOper.get_hospital_clinic_base_info_by_clinic_id(clinic_id):
        # TODO storage-info 插入日志：新增
        HospitalClinicBaseInfoOper.add_one(hospital_clinic_base_info)
    else:
        # TODO storage-info 日志：已存在并更新
        HospitalClinicBaseInfoOper.add_one(hospital_clinic_base_info)
    # TODO storage-error 日志-插入失败