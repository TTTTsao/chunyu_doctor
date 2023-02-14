import json
from lxml import etree
from bs4 import BeautifulSoup
from spider.db.models import *
from spider.db.dao.hospital_dao import *
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import *
from spider.util.basic import trans_to_datetime
from spider.util.reg.reg_doctor import *
from spider.util.reg.reg_hospital import *
from spider.util.log_util import create_parse_logger
logger = create_parse_logger()
logger.remove()

@parse_decorator(False)
def hospital_page_html_2_realtime_inquiry_nums(hospital_id, html):
    '''
    根据医院详情页解析医院可实时咨询医生数
    :param hospital_id: 医院id
    :param html: 医院详情页
    :return: 可实时咨询医生数对象
    '''
    xpath = etree.HTML(html)
    try:
        inquiry_nums = xpath.xpath("//span[@class='light'][2]/text()")[0]
        return HospitalRealTimeInquiry(
            hospital_id=hospital_id,
            real_time_inquiry_doctor_num=int(inquiry_nums)
        )
    except Exception as e:
        logger.error("解析医院 {} 可实时咨询医生数失败，详情: {}".format(hospital_id, e))
        return HospitalRealTimeInquiry(
            hospital_id=hospital_id,
            real_time_inquiry_doctor_num=0
        )

@parse_decorator(False)
def hospital_rank_page_html_2_hospital_rank(area_id, clinic_id, html):
    if '医院排名暂无数据' in html:
        logger.warning("地区 {} 暂无 {} 科室排名".format(area_id, clinic_id))
        return None
    xpath = etree.HTML(html)
    try:
        
        pass
    except Exception as e:
        logger.error("解析地区 {} 科室 {} 排名失败，详情: {}".format(area_id, clinic_id, e))
        return None