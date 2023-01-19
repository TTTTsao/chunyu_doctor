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
    # TODO crawl-info 正在抓取xx医院医生当前在线可咨询信息
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_real_time_inquiry_data = get_hospital_real_time_inquiry(hospital_id, html)
    # 不存在
    if not hospital_real_time_inquiry_data:
        # TODO parse-waring 日志警告 不存在医生当前在线可咨询信息
        return
    # 不存在于表
    if not HospitalRealTimeInquiryOper.get_hospital_realtime_inquiry_by_hospital_id(hospital_id):
        # TODO storage-info 插入日志：新增
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)
    else:
        # TODO storage-info 日志：已存在并更新
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)
    # TODO storage-error 日志-插入失败