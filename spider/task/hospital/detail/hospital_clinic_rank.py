from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalClinicRankOper
from spider.page_parse.hospital.hospital_clinic_rank import get_hospital_clinic_rank
from loguru import logger
from spider.decorators.crawl_decorator import crawl_decorator

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

@crawl_decorator
def crawl_hospitall_clinic_rank(hospital_id):
    '''
    根据hospital_id爬取医院各科室排名信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医院科室排名信息".format(hospital_id))

    hospital_clinic_rank_datas = get_hospital_clinic_rank(hospital_id, html)
    # 不存在
    if not hospital_clinic_rank_datas:
        logger.warning(" {} 医院不存在科室排名信息".format(hospital_id))
        return
    HospitalClinicRankOper.add_all(hospital_clinic_rank_datas)