from bs4 import BeautifulSoup

from spider.page_get.basic import get_page_html
from spider.page_parse.hospital import (get_hospital_base_info, get_hospital_enter_doctor_info, get_hospital_real_time_inquiry,
                                        get_hospital_clinic_base_info, get_hospital_clinic_rank, get_hospital_province_list,
                                        get_hospital_list_from_province,get_clinic_id_list)
from spider.db.dao.hospital_dao import *

BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_RANK_URL = 'https://chunyuyisheng.com//pc/hospitallist/{}/{}'

def crawl_all_hospital_base_info():
    '''
    抓取所有医院信息（基本信息、医生入驻信息、当前在线咨询信息、医院科室排名信息）
    :return:
    '''

    # 获取所有省份id：get_hospital_province_list
    province_list_html = get_page_html(BASE_URL)
    province_list = get_hospital_province_list(province_list_html)

    # 遍历获得每个省份下的医院id：get_hospital_list_from_province
    for i in range(len(province_list)):
        print('正在抓取第', i, "页", province_list[i])
        province_url = HOSPITAL_URL.format(province_list[i])
        hospital_list_html = get_page_html(province_url)

        hospital_list = get_hospital_list_from_province(hospital_list_html)
        for hospital in hospital_list:
            print("正在抓取医院", hospital[0])
            id = hospital[0]
            city = hospital[1]

            # 进入每个医院详情页
            # crawl_hospitall_clinic_rank(id)
            # crawl_hospital_base_info(id, city)
            # crawl_hospital_clinic_enter_doctor(id)
            crawl_hospital_real_time_inquiry(id)

        print("第", i, "页数据抓取完毕")


def crawl_all_hospital_clinic_base_info():
    '''
    TODO 抓取所有医院的所有科室基本信息
    1. 获取所有省份id
    2. 获取所有医院id
    3. 进入医院详情页
    4. 获取所有科室id信息，并进入遍历获取信息
    :return:
    '''
    # 1 获取所有省份id：get_hospital_province_list
    province_list_html = get_page_html(BASE_URL)
    province_list = get_hospital_province_list(province_list_html)

    # 2 遍历获得每个省份下的医院id：get_hospital_list_from_province
    for i in range(len(province_list)):
        print('正在抓取第', i, "页", province_list[i])
        province_url = HOSPITAL_URL.format(province_list[i])
        hospital_list_html = get_page_html(province_url)

        hospital_list = get_hospital_list_from_province(hospital_list_html)
        for hospital in hospital_list:
            print("正在抓取医院", hospital[0])
            id = hospital[0]

            # 3 进入每个医院详情页
            hospital_url = HOSPITAL_DETAIL_URL.format(id)
            html = get_page_html(hospital_url)
            # 4 获取clinic id并遍历
            clinic_id_list = get_clinic_id_list(html)
            for clinic_id in clinic_id_list:
                print("正在抓取科室", clinic_id)
                crawl_hospital_clinic_base_info(clinic_id)

        print("第", i, "页数据抓取完毕")


def crawl_hospital_base_info(hospital_id, city):
    '''
    根据hospital_id爬取医院基本信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_base_data = get_hospital_base_info(hospital_id, city, html)
    # 不存在
    if not hospital_base_data:
        # 日志警告
        return

    # 不存在于表
    if not HospitalOper.get_hospital_base_info_by_hospital_id(hospital_id):
        # 插入日志：新增
        HospitalOper.add_one(hospital_base_data)
    else:
        # 日志：已存在并更新
        HospitalOper.add_one(hospital_base_data)


def crawl_hospital_clinic_enter_doctor(hospital_id):
    '''
    根据hospital_id爬取医院医生入驻信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_enter_data = get_hospital_enter_doctor_info(hospital_id, html)
    # 不存在
    if not hospital_enter_data:
        # 日志警告
        return

    # 不存在于表
    if not HospitalClinicEnterDoctorOper.get_hosital_clinic_enter_doctor_by_hospital_id(hospital_id):
        # 插入日志：新增
        HospitalClinicEnterDoctorOper.add_all(hospital_enter_data)
    else:
        # 日志：已存在并更新
        HospitalClinicEnterDoctorOper.add_all(hospital_enter_data)

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
        # 日志警告
        return
    # 不存在于表
    if not HospitalRealTimeInquiryOper.get_hospital_realtime_inquiry_by_hospital_id(hospital_id):
        # 插入日志：新增
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)
    else:
        # 日志：已存在并更新
        HospitalRealTimeInquiryOper.add_one(hospital_real_time_inquiry_data)


def crawl_hospital_clinic_base_info(clinic_id):
    '''
    根据clinic_id爬取医院科室基本信息
    :param hospital_id:
    :return:
    '''
    url = HOSPITAL_CLINIC_URL.format(clinic_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_clinic_base_info = get_hospital_clinic_base_info(clinic_id, html)
    # 不存在
    if not hospital_clinic_base_info:
        # 日志警告
        return
    # 不存在于表
    if not HospitalClinicBaseInfoOper.get_hospital_clinic_base_info_by_clinic_id(clinic_id):
        # 插入日志：新增
        HospitalClinicBaseInfoOper.add_one(hospital_clinic_base_info)
    else:
        # 日志：已存在并更新
        HospitalClinicBaseInfoOper.add_one(hospital_clinic_base_info)


def crawl_hospitall_clinic_rank(hospital_id):
    '''
    根据hospital_id爬取医院各科室排名信息
    :param hospital_id:
    :return:
    '''
    # print("进入")
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_clinic_rank_datas = get_hospital_clinic_rank(hospital_id, html)
    # 不存在
    if not hospital_clinic_rank_datas:
        # 日志警告
        return
    # 不存在于表
    if not HospitalClinicRankOper.get_hospital_clinic_rank_by_hospital_id(hospital_id):
        # 插入日志：新增
        HospitalClinicRankOper.add_all(hospital_clinic_rank_datas)
    else:
        # 日志：已存在并更新
        HospitalClinicRankOper.add_all(hospital_clinic_rank_datas)


def crawl_hospital_rank():
    '''
    TODO 抓取医院综合排名信息
    未定所需要的参数
    :return:
    '''

if __name__ == '__main__':
    crawl_all_hospital_base_info()