from spider.page_get.basic import get_page_html
from spider.task.hospital.detail.hospital_base_info import crawl_hospital_base_info
from spider.task.hospital.detail.hospital_clinic_base_info import crawl_hospital_clinic_base_info
from spider.task.hospital.detail.enter_doctor import crawl_hospital_clinic_enter_doctor
from spider.task.hospital.detail.real_time_inquiry import crawl_hospital_real_time_inquiry
from spider.task.hospital.detail.hospital_clinic_rank import crawl_hospitall_clinic_rank
from spider.page_parse.hospital.basic import (get_hospital_province_list,
                                              get_hospital_list_from_province,
                                              get_clinic_id_list)


BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

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
        # TODO crawl-info 日志 正在抓取xx地区的医院信息
        print('正在抓取第', i, "页", province_list[i])
        province_url = HOSPITAL_URL.format(province_list[i])
        hospital_list_html = get_page_html(province_url)

        hospital_list = get_hospital_list_from_province(hospital_list_html)
        for hospital in hospital_list:
            # TODO crawl-info 正在抓取xx医院的信息
            print("正在抓取医院", hospital[0])
            id = hospital[0]
            city = hospital[1]

            # 进入每个医院详情页
            # crawl_hospitall_clinic_rank(id)
            # crawl_hospital_base_info(id, city)
            crawl_hospital_clinic_enter_doctor(id)
            crawl_hospital_real_time_inquiry(id)

        # TODO crawl-info xxx地区医院信息已抓取完毕
        print("第", i, "页数据抓取完毕")

def crawl_all_hospital_clinic_base_info():
    '''
    抓取所有医院的所有科室基本信息
    1. 获取所有省份id
    2. 获取所有医院id
    3. 进入医院详情页
    4. 获取所有科室id信息，并进入遍历获取信息
    :return:
    '''
    # 1 获取所有省份id：get_hospital_province_list
    province_list_html = get_page_html(BASE_URL)
    province_list = get_hospital_province_list(province_list_html)
    # province_list = ['120000-0', '130000-0', '140000-0',
    #                 '150000-0', '210000-0', '220000-0', '230000-0',
    #                 '310000-0', '320000-0', '330000-0', '340000-0',
    #                 '350000-0', '360000-0', '370000-0', '410000-0',
    #                 '420000-0', '430000-0', '440000-0', '450000-0',
    #                 '460000-0', '500000-0', '510000-0', '520000-0',
    #                 '530000-0', '540000-0', '610000-0', '620000-0',
    #                 '630000-0', '640000-0', '650000-0', '710000-0']

    # 2 遍历获得每个省份下的医院id：get_hospital_list_from_province
    for i in range(len(province_list)):
        # TODO crawl-info 日志 正在抓取xx地区的医院科室信息
        print('正在抓取第', i, "页", province_list[i])
        province_url = HOSPITAL_URL.format(province_list[i])
        hospital_list_html = get_page_html(province_url)

        hospital_list = get_hospital_list_from_province(hospital_list_html)
        for hospital in hospital_list:
            # TODO crawl-info 日志 正在抓取xx医院信息
            print("正在抓取医院", hospital[0])
            id = hospital[0]

            # 3 进入每个医院详情页
            hospital_url = HOSPITAL_DETAIL_URL.format(id)
            html = get_page_html(hospital_url)

            # 4 获取clinic id并遍历
            clinic_id_list = get_clinic_id_list(html)
            if not clinic_id_list:
                # TODO crawl-warning 该页面科室列表信息为空
                print("clinic_id_list", clinic_id_list)
                # 日志警告
            else:
                for clinic_id in clinic_id_list:
                    # TODO crawl-info 正在抓取xx科室信息
                    print("正在抓取科室", clinic_id)
                    crawl_hospital_clinic_base_info(clinic_id)

        # TODO crawl-info xxx地区医院科室信息已抓取完毕
        print("第", i, "页数据抓取完毕")

def crawl_hospital_by_province_list(province_list):
    '''
    根据省份list抓取各个省份list
    :param province_list:
    :return:
    '''
    if len(province_list) == 1:
        crawl_hospital_by_province(province_list[0])
    else:
        for i in range(len(province_list)):
            crawl_hospital_by_province(province_list[i])


def crawl_hospital_by_province(province_id):
    '''
    根据省份id抓取医院信息
    :param province_id:
    :return:
    '''
    province_url = HOSPITAL_URL.format(province_id)
    hospital_list_html = get_page_html(province_url)
    # TODO crawl-info 日志 开始抓取xx地区医院信息
    # crawler.info('the crawling url is {url}'.format(url=url))

    hospital_list = get_hospital_list_from_province(hospital_list_html)
    for hospital in hospital_list:
        # TODO crawl-info 日志 开始抓取xx医院
        print("正在抓取医院", hospital[0])
        id = hospital[0]
        city = hospital[1]

        # 进入每个医院详情页
        crawl_hospitall_clinic_rank(id)
        crawl_hospital_base_info(id, city)
        crawl_hospital_clinic_enter_doctor(id)
        crawl_hospital_real_time_inquiry(id)