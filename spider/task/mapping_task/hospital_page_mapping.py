import random
import time

from spider.db.dao.hospital_dao import *

from spider.page_get.chunyu_request import hospital_page_request as hr
from spider.page_parse.field_parse import hospital_parse as hp
from spider.page_parse.basic import *
from spider.decorators.crawl_decorator import crawl_decorator
from spider.util.basic import (check_db_exist, check_db_today, check_db_interval)
from spider.util.log_util import create_crawl_logger
logger = create_crawl_logger()
logger.remove()

@crawl_decorator
def hospital_high_frequency_mapping(hospital_id):
    '''
    【医院高频更新信息-每4个小时】
    包含：
    [医院可实时咨询医生数量]
    :param hospital_id: 医院id
    :return:
    '''
    html = hr.get_hospital_deatil_page(hospital_id)
    if html is None:
        logger.warning("医院 {} 页面为None".format(hospital_id))
    elif is_404(html):
        logger.warning("医院 {} 页面为 404 页面".format(hospital_id))
    else:
        hospital_real_time_inquiry_data = hp.hospital_page_html_2_realtime_inquiry_nums(hospital_id, html)
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)

@crawl_decorator
def hospital_detail_page_mapping(hospital_id):
    '''
    医院详情页面信息
    包含：
    【医院基本信息 base_info】
    【医院科室医生入驻信息 enter_info】
    【医院各科室排名信息 clinic_rank】
    【医院可实时咨询医生数量 real_time_inquiry】
    :param hospital_id: 医院id
    :return:
    '''
    html = hr.get_hospital_deatil_page(hospital_id)
    if html is None:
        logger.warning("医院 {} 页面为None".format(hospital_id))
    elif is_404(html):
        logger.warning("医院 {} 页面为 404 页面".format(hospital_id))
    else:
        base_data = hp.hospital_page_html_2_hospital_base_info(hospital_id, html)
        enter_data = hp.hospital_page_html_2_hospital_clinic_enter_info(hospital_id, html)
        # clinic_rank =

    pass

