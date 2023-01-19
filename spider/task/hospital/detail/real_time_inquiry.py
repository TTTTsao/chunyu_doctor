from spider.page_get.basic import get_page_html
from spider.db.dao.hospital_dao import HospitalRealTimeInquiryOper
from spider.page_parse.hospital.real_time_inquiry import get_hospital_real_time_inquiry

HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

def crawl_hospital_real_time_inquiry(hospital_id):
    '''
    根据hospital_id爬取医院医生当前在线可咨询信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_real_time_inquiry_data = get_hospital_real_time_inquiry(hospital_id, html)
    # 不存在
    if not hospital_real_time_inquiry_data:
        # TODO 日志警告
        return
    # 不存在于表
    if not HospitalRealTimeInquiryOper.get_hospital_realtime_inquiry_by_hospital_id(hospital_id):
        # TODO 插入日志：新增
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)
    else:
        # TODO 日志：已存在并更新
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)