from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.price import *

from spider.db.dao.doctor_dao import DoctorPriceOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_price(doctor_id):
    '''
    抓取医生价格信息（id、价格、折扣【需判断有无】、类型）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    # TODO crawl-info 正在抓取xx医生价格信息
    # crawler.info('the crawling url is {url}'.format(url=url))
    doctor_price_data = get_doctor_price(doctor_id, html)

    # 不存在
    if not doctor_price_data:
        # TODO parse-waring 日志警告 不存在价格信息
        return

    if not DoctorPriceOper.get_doctor_price_by_doctor_id(doctor_id):
        # TODO storage-info 插入日志：新增
        DoctorPriceOper.add_one(doctor_price_data)
    else:
        # TODO storage-info 日志：已存在并更新
        DoctorPriceOper.add_one(doctor_price_data)
    # TODO storage-error 日志-插入失败

