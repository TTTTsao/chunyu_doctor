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
def hospital_page_html_2_hospital_base_info(hospital_id, html):
    '''
    根据医院详情页抓取医院基本信息
    :param hospital_id: 医院id
    :param html: 医院详情页
    :return: 医院base_info对象/None（错误）
    '''
    xpath = etree.HTML(html)
    try:
        name = xpath.xpath("//div[@class='content-title']/h3/text()")[0]
        bread_list = xpath.xpath("//ul[@class='bread-crumb']/li/a/text()")
        profile = xpath.xpath("//div[@class='content-info']/div[1]/p/text()")
        tag_dic = {}
        tag_dic["rank"] = xpath.xpath("//div[@class='content-title']/span[1]/text()")[0]
        tag_dic["type"] = xpath.xpath("//div[@class='content-title']/span[2]/text()")[0]
        return Hospital(
            hospital_id=hospital_id,
            hospital_name=name,
            hospital_area=bread_list[1],
            hospital_province=bread_list[2],
            hospital_city=bread_list[3] if len(bread_list == 4) else None,
            hospital_profile=get_reg_hospital_profile(str(profile)),
            hospital_tag=json.dumps(tag_dic, ensure_ascii=False)
        )
    except Exception as e:
        logger.error("解析医院 {} 详情页面医院base info信息失败，错误详情 {}".format(hospital_id, e))
        return None


@parse_decorator(False)
def hospital_page_html_2_hospital_clinic_enter_info(hospital_id, html):
    '''
    根据医院详情页抓取医院科室入驻人数
    :param hospital_id: 医院id
    :param html: 医院详情页
    :return: 医院clinic_enter_info对象/None（错误）
    '''
    xpath = etree.HTML(html)
    flag = is_page_has_no_info(html)
    try:
        row_clinic_id_list = xpath.xpath('//*[@id="clinic"]/li/a/@href')
        row_enter_nums_list = xpath.xpath('//*[@id="clinic"]/li/span/i/text()')
        if flag and len(row_clinic_id_list) == 0: return HospitalClinicEnterDoctor(hospital_id=hospital_id, hospital_clinic_id="无入驻科室")
        elif len(row_clinic_id_list) > 0:
            hospital_enter_datas = []
            for i in range(len(row_clinic_id_list)):
                hospital_enter_datas.append(HospitalClinicEnterDoctor(
                    hospital_id=hospital_id,
                    hospital_clinic_id=get_reg_clinic_id(str(row_clinic_id_list[i])),
                    hospital_clinic_amount=0 if ((i-len(row_enter_nums_list))>-1) else int(row_enter_nums_list[i])
                ))
            return hospital_enter_datas
        else: return HospitalClinicEnterDoctor(hospital_id=hospital_id, hospital_clinic_id="无入驻科室")
    except Exception as e:
        logger.error("解析医院 {} 详情页面医院科室入驻人数信息失败，错误详情 {}".format(hospital_id, e))
        return None

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
        inquiry_nums = xpath.xpath("//span[@class='light'][2]/text()")
        return HospitalRealTimeInquiry(
            hospital_id=hospital_id,
            real_time_inquiry_doctor_num=int(inquiry_nums[0]) if (len(inquiry_nums)!=0) else 0
        )
    except Exception as e:
        logger.error("解析医院 {} 可实时咨询医生数失败，详情: {}".format(hospital_id, e))
        return HospitalRealTimeInquiry(
            hospital_id=hospital_id,
            real_time_inquiry_doctor_num=0
        )

@parse_decorator(False)
def hospital_clinic_page_html_2_hospital_clinic_base_info(clinic_id, html):
    '''
    根据科室页面获取科室基本信息
    :param clinic_id: 医院科室id
    :param html: 医院科室详情页面
    :return: 医院科室基本信息对象/None（错误）
    '''
    xpath = etree.HTML(html)
    try:
        name = xpath.xpath("//h3[@class='title']//text()")
        row_profile = xpath.xpath("//div[@class='content-info']/div/p/text()")
        return HospitalClinicBaseInfo(
            hospital_clinic_id=clinic_id,
            hospital_clinic_name=name[0] if (len(name) !=0 ) else None,
            hospital_clinic_profile=get_reg_clinic_profile(str(row_profile)) if (len(row_profile) != 0) else None
        )
    except Exception as e:
        logger.error("解析医院科室 {} 基本信息失败，详情: {}".format(clinic_id, e))
        return None

@parse_decorator(False)
def hospital_clinic_page_html_2_doctor_base_and_img(clinic_id, html):
    '''
    根据科室页面获取医生列表的医生base_info和img
    :param clinic_id: 医院科室id
    :param html: 医院科室详情页面
    :return: 医生base_info对象+img对象/None+None（错误）
    '''
    if is_page_has_no_info(html): return None, None
    xpath = etree.HTML(html)
    base_datas = [], img_datas = []
    try:
        doctor_id_list = xpath.xpath("//div[@class='doctor-wrap']/div/div/div[1]/a/@href")
        doctor_name_list = xpath.xpath("//div[@class='doctor-wrap']/div/div/div[2]/div/a/span[1]/text()")
        doctor_img_url_list = xpath.xpath("//div[@class='doctor-wrap']/div/div/div[1]/a/img/@src")
        for i in range(len(doctor_id_list)):
            base_datas.append(DoctorBaseInfo(doctor_id=get_reg_doctor_id(str(doctor_id_list[i])), doctor_name=get_reg_doctor_name(str(doctor_name_list[i]))))
            img_datas.append(DoctorImg(doctor_id=get_reg_doctor_id(str(doctor_id_list[i])), doctor_img_remote_path=str(doctor_img_url_list[i])))
        return base_datas, img_datas
    except Exception as e:
        logger.error("解析医院科室 {} 医生列表信息失败，详情: {}".format(clinic_id, e))
        return None, None


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