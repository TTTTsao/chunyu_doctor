from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalOper
from spider.page_parse.hospital.hospital_base_info import get_hospital_base_info

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

def crawl_hospital_base_info(hospital_id, city):
    '''
    根据hospital_id爬取医院基本信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # TODO crawl-info 日志-开始抓取xx医院基本信息
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_base_data = get_hospital_base_info(hospital_id, city, html)
    # 不存在
    if not hospital_base_data:
        # TODO crawl-warning日志警告-该医院不存在基本信息
        return

    # 不存在于表
    if not HospitalOper.get_hospital_base_info_by_hospital_id(hospital_id):
        # TODO storage-info 插入日志：新增
        HospitalOper.add_one(hospital_base_data)
    else:
        # TODO storage-info 插入日志：已存在并更新
        HospitalOper.add_one(hospital_base_data)
    # TODO storage-error 日志-插入失败