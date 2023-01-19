from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalClinicRankOper
from spider.page_parse.hospital.hospital_clinic_rank import get_hospital_clinic_rank

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

def crawl_hospitall_clinic_rank(hospital_id):
    '''
    根据hospital_id爬取医院各科室排名信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_clinic_rank_datas = get_hospital_clinic_rank(hospital_id, html)
    # 不存在
    if not hospital_clinic_rank_datas:
        # TODO 日志警告
        return
    # 不存在于表
    if not HospitalClinicRankOper.get_hospital_clinic_rank_by_hospital_id(hospital_id):
        # TODO 插入日志：新增
        HospitalClinicRankOper.add_all(hospital_clinic_rank_datas)
    else:
        # TODO 日志：已存在并更新
        HospitalClinicRankOper.add_all(hospital_clinic_rank_datas)