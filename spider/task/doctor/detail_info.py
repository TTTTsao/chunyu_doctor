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
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

logging_format = get_logger_logging_format()

logger.add(sys.stderr, level="INFO", format=logging_format)
logger.add('spider/logs/crawl_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/crawl_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/crawl_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')


BASE_URL = 'https://chunyuyisheng.com/pc/doctors/?page={}'

HOSPITAL_BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_CLINIC_PAGE_URL = 'https://chunyuyisheng.com/pc/clinic/{}/?page={}'

@crawl_decorator
def crawl_all_doctor_detail_info():
    '''
    抓取所有医生详情页信息（认证信息、标签信息、服务信息、价格信息、简介信息、好评信息、心意墙信息）
    1.遍历所有医院 2.遍历医院的所有科室 3.获取科室的所有医生id 4.根据id format url并抓取详情页信息
    :return:
    '''
    # 获取所有省份id：get_hospital_province_list
    province_list = ['650000-0', '130000-0', '140000-0', '710000-0'
                     '150000-0', '210000-0', '220000-0', '230000-0',
                     '310000-0', '320000-0', '330000-0', '340000-0',
                     '350000-0', '360000-0', '370000-0', '410000-0',
                     '420000-0', '430000-0', '440000-0', '450000-0',
                     '460000-0', '500000-0', '510000-0', '520000-0',
                     '530000-0', '540000-0', '610000-0', '620000-0',
                     '630000-0', '640000-0', '120000-0', '110000-0']

    # 遍历获得每个省份下的医院id：get_hospital_list_from_province
    for i in range(len(province_list)):
        logger.info("正在抓取第 {} 个 省份 {} 的医院列表".format(i+1, province_list[i]))
        province_url = HOSPITAL_URL.format(province_list[i])
        hospital_list_html = get_page_html(province_url)

        hospital_list = get_hospital_list_from_province(hospital_list_html)
        if not hospital_list:
            logger.error("无法获取 {} 省份的医院列表信息".format(province_list[i]))
            return
        for hospital in hospital_list:
            logger.info("正在抓取医院 {} 的医生详细信息")

            # 进入每个医院详情页
            hospital_url = HOSPITAL_DETAIL_URL.format(id)
            html = get_page_html(hospital_url)
            # 4 获取clinic id并遍历
            clinic_id_list = get_clinic_id_list(html)
            if not clinic_id_list:
                logger.warning("医院 {} 无可获取的科室信息".format(hospital))
            else:
                for clinic_id in clinic_id_list:
                    logger.info("正在抓取科室 {} 的医生详情信息".format(clinic_id))
                    crawl_doctor_detail_info_from_clinic(clinic_id)
        logger.info("正在完成第 {} 个 省份的医生详细信息抓取".format(i+1))

@crawl_decorator
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
    try:
        clinic_doctor_nums = xpath.xpath("//div[@class='doctor-number']/span[2]/text()")
    except Exception as e:
        logger.error("获取 {} 科室的医生数量失败，错误详情：{}".format(clinic_id, e))
        return

    # 判断页面医生暂无的情况
    if is_page_has_no_doctor_nums(clinic_html, clinic_doctor_nums):
        return

    if 0 < int(clinic_doctor_nums[0]) <= 20:
        # 获取doctor id list, 然后进入详情页进行抓取
        doctor_id_list = get_doctor_id_list_from_clinic_page(clinic_html)
        if not doctor_id_list:
            logger.warning(" 无法获取 {} 科室 的医生列表".format(clinic_id))
            return
        for doctor_id in doctor_id_list:
            crawl_doctor_detail_info(doctor_id)
    else:
        max_page = math.ceil(int(clinic_doctor_nums[0]) / 20)
        cur_page = 1
        while cur_page <= max_page:
            logger.info("正在爬取 {} 科室 第 {} 页数据".format(clinic_id, cur_page))
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
            if not doctor_id_list:
                logger.error(" 获取 {} 科室 的医生列表失败".format(clinic_id))
            for doctor_id in doctor_id_list:
                crawl_doctor_detail_info(doctor_id)

            cur_page += 1

@crawl_decorator
def crawl_active_doctor_detail_info():
    '''
    通过【根据科室找医生】抓取活跃的医生id list
    format url后抓取详情信息
    :return:
    '''
    # 爬取 26 个活跃医生页（共20*26个医生信息）
    limit = get_max_home_page()
    cur_page = 1

    # TODO 增加【当前页面数据】与【前一页数据】相同，跳出循环的判断
    while cur_page <= limit:
        logger.info("正在爬取第 {} 页数据".format(cur_page))
        url = BASE_URL.format(cur_page)
        html = get_page_html(url)

        doctor_id_list = get_active_doctor_id_list(html)

        for i in range(len(doctor_id_list)):
            doctor_id = doctor_id_list[i]
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

@crawl_decorator
def crawl_doctor_detail_info(doctor_id):
    '''
    通过【医生个人详情页】抓取所有详情信息
    :param doctor_id:
    :return:
    '''
    logger.info("正在抓取 医生 {} 的所有详情信息".format(doctor_id))

    crawl_doctor_auth_info(doctor_id)
    crawl_doctor_tag(doctor_id)
    crawl_doctor_service_info(doctor_id)
    # crawl_doctor_price(doctor_id)
    crawl_doctor_description(doctor_id)
    crawl_doctor_comment_label(doctor_id)
    # crawl_illness_question(doctor_id)
    crawl_doctor_reward(doctor_id)

