import math

from spider.page_get.basic import get_page_html
from spider.page_parse.basic import (is_page_has_no_doctor_nums)
from spider.page_parse.doctor.basic import *
from spider.task.doctor.detail.auth_info import crawl_doctor_auth_info
from spider.task.doctor.detail.reward import crawl_doctor_reward
from spider.task.doctor.detail.tag import crawl_doctor_tag
from spider.task.doctor.detail.illness import crawl_illness_question
from spider.task.doctor.detail.price import crawl_doctor_price
from spider.task.doctor.detail.comment_label import crawl_doctor_comment_label
from spider.task.doctor.detail.service_info import crawl_doctor_service_info
from spider.task.doctor.detail.description import crawl_doctor_description
from spider.page_parse.hospital.basic import (get_hospital_province_list, get_hospital_list_from_province, get_clinic_id_list)

from spider.config.conf import (get_max_home_page)

BASE_URL = 'https://chunyuyisheng.com/pc/doctors/?page={}'

HOSPITAL_BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_CLINIC_PAGE_URL = 'https://chunyuyisheng.com/pc/clinic/{}/?page={}'

def crawl_all_doctor_detail_info():
    '''
    TODO 抓取所有医生详情页信息（认证信息、标签信息、服务信息、价格信息、简介信息、好评信息、心意墙信息）
    1.遍历所有医院 2.遍历医院的所有科室 3.获取科室的所有医生id 4.根据id format url并抓取详情页信息
    :return:
    '''
    # 获取所有省份id：get_hospital_province_list
    province_list_html = get_page_html(HOSPITAL_BASE_URL)
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

            # 进入每个医院详情页
            hospital_url = HOSPITAL_DETAIL_URL.format(id)
            html = get_page_html(hospital_url)
            # 4 获取clinic id并遍历
            clinic_id_list = get_clinic_id_list(html)
            if not clinic_id_list:
                print("clinic_id_list", clinic_id_list)
                # 日志警告
            else:
                for clinic_id in clinic_id_list:
                    print("正在抓取科室", clinic_id)
                    # TODO 抓取每个科室的医生id用于获取医生详情页相关信息
                    crawl_doctor_detail_info_from_clinic(clinic_id)

        print("第", i, "页数据抓取完毕")

def crawl_doctor_detail_info_from_clinic(clinic_id):
    '''
    在科室详情页抓取该科室所有医生的id并进入医生详情页抓取详情信息
    1. 进入clinic detail url
    2. 获取当前科室人数，> 20则需要遍历，<=20抓取当前的基本信息并add_all
    3. while 遍历获取当前页面的医生基本信息 get_doctor_id_from_clinic
    :param clinic_id:
    :return:
    '''
    clinic_url = HOSPITAL_CLINIC_URL.format(clinic_id)
    clinic_html = get_page_html(clinic_url)
    xpath = etree.HTML(clinic_html)

    if not clinic_html:
        return
    clinic_doctor_nums = xpath.xpath("//div[@class='doctor-number']/span[2]/text()")

    # 判断页面医生暂无的情况
    if is_page_has_no_doctor_nums(clinic_html, clinic_doctor_nums):
        return

    if 0 < int(clinic_doctor_nums[0]) <= 20:
        # 获取doctor id list, 然后进入详情页进行抓取
        doctor_id_list = get_doctor_id_list_from_clinic_page(clinic_html)
        for doctor_id in doctor_id_list:
            crawl_doctor_detail_info(doctor_id)
    else:
        max_page = math.ceil(int(clinic_doctor_nums[0]) / 20)
        cur_page = 1
        while cur_page <= max_page:
            # TODO crawl-info
            # print("正在爬取,", clinic_id, "第", cur_page, "页数据")
            url = HOSPITAL_CLINIC_PAGE_URL.format(clinic_id, cur_page)
            html = get_page_html(url)
            xpath = etree.HTML(html)
            if not html:
                return
            page_doctor_nums = xpath.xpath("//div[@class='doctor-number']/span[2]/text()")

            if is_page_has_no_doctor_nums(html, page_doctor_nums):
                cur_page += 1
                return
            # 获取doctor id 并进入详情页进行抓取
            doctor_id_list = get_doctor_id_list_from_clinic_page(html)
            for doctor_id in doctor_id_list:
                crawl_doctor_detail_info(doctor_id)

            cur_page += 1

def crawl_active_doctor_detail_info():
    '''
    通过【根据科室找医生】抓取活跃的医生id list
    format url后抓取详情信息
    :return:
    '''
    # 爬取 30 个活跃医生页（共20*30个医生信息）
    limit = get_max_home_page()
    cur_page = 1

    # TODO 增加【当前页面数据】与【前一页数据】相同，跳出循环的判断
    while cur_page <= limit:
        print("正在爬取第", cur_page, "页数据")
        url = BASE_URL.format(cur_page)
        html = get_page_html(url)

        doctor_id_list = get_active_doctor_id_list(html)

        for i in range(len(doctor_id_list)):
            doctor_id = doctor_id_list[i]
            # print("开始抓取", doctor_id, "的详情页")
            crawl_doctor_auth_info(doctor_id)
            crawl_doctor_tag(doctor_id)
            crawl_doctor_service_info(doctor_id)
            crawl_doctor_price(doctor_id)
            crawl_doctor_description(doctor_id)
            crawl_doctor_comment_label(doctor_id)
            crawl_illness_question(doctor_id)
            crawl_doctor_reward(doctor_id)
        # TODO 增加发生错误，存储该doctor_id用于稍后重新抓取

        cur_page += 1

def crawl_doctor_detail_info(doctor_id):
    '''
    通过【医生个人详情页】抓取所有详情信息
    :param doctor_id:
    :return:
    '''
    print("正在抓取医生", doctor_id)

    # crawl_doctor_auth_info(doctor_id)
    # crawl_doctor_tag(doctor_id)
    crawl_doctor_service_info(doctor_id)
    crawl_doctor_price(doctor_id)
    # crawl_doctor_description(doctor_id)
    crawl_doctor_comment_label(doctor_id)
    crawl_illness_question(doctor_id)
    crawl_doctor_reward(doctor_id)

