import math

from spider.page_get.basic import get_page_html
from spider.page_parse.basic import is_404
from spider.page_parse.doctor import *
from spider.page_parse.hospital import (get_hospital_province_list, get_hospital_list_from_province, get_clinic_id_list)

from spider.logger import crawler, storage
from spider.db.dao.doctor_dao import *
from spider.config.conf import (get_max_home_page)


BASE_URL = 'https://chunyuyisheng.com/pc/doctors/?page={}'
DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'
ILLNESS_AJAX_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}/qa/?is_json=1&tag={}&page_count=20&page={}'

HOSPITAL_BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_CLINIC_PAGE_URL = 'https://chunyuyisheng.com/pc/clinic/{}/?page={}'



def crawl_all_doctor_base_info():
    '''
    # TODO 抓取所有医生的基本信息（id、name）和头像信息（id，img_url）
    1.遍历所有省份 2.遍历所有医院 3.获取科室的所有医生id 4.进入科室详情抓取医生基本信息
    :return:
    '''
    # 获取所有省份id：get_hospital_province_list
    province_list = ['220000-0', '230000-0', '310000-0', '320000-0', '330000-0', '340000-0',
                     '350000-0', '360000-0', '370000-0', '410000-0', '420000-0', '430000-0',
                     '440000-0', '450000-0', '460000-0', '500000-0', '510000-0', '520000-0',
                     '530000-0', '540000-0', '610000-0', '620000-0', '630000-0', '640000-0',
                     '650000-0', '710000-0']

    # province_list_html = get_page_html(HOSPITAL_BASE_URL)
    # province_list = get_hospital_province_list(province_list_html)

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
                    crawl_doctor_base_info_from_clinic(clinic_id)

        print("第", i, "页数据抓取完毕")



def crawl_doctor_base_info_from_clinic(clinic_id):
    '''
    在科室详情页抓取该科室所有医生的基本信息和头像信息（id、name和img）
    1. 进入clinic detail url
    2. 获取当前科室人数，> 20则需要遍历，<=20抓取当前的基本信息并add_all
    3. while 遍历获取当前页面的医生基本信息 get_doctor_base_info_from_clinic
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
    try:
        if '暂无相关信息' in clinic_html:
            # 日志记录
            print("暂无相关信息")
            return False
        elif len(clinic_doctor_nums) == 0:
            print("该页面无人数板块")
            return
        elif int(clinic_doctor_nums[0]) == 0:
            print("该科室没有人")
            return
        elif is_404(clinic_html):
            return
    except AttributeError:
        return False

    if 0 < int(clinic_doctor_nums[0]) <= 20:
        doctor_base_datas = get_doctor_base_info_from_clinic(clinic_html)
        doctor_img_datas = get_doctor_img_from_clinic(clinic_html)

        DoctorBaseInfoOper.add_all(doctor_base_datas)
        DoctorImgOper.add_all(doctor_img_datas)
    else:
        max_page = math.ceil(int(clinic_doctor_nums[0]) / 20)
        cur_page = 1
        while cur_page <= max_page:
            print("正在爬取,", clinic_id, "第", cur_page, "页数据")
            url = HOSPITAL_CLINIC_PAGE_URL.format(clinic_id, cur_page)
            html = get_page_html(url)

            try:
                if '暂无相关信息' in html:
                    # 日志记录
                    print("暂无相关信息")
                    cur_page += 1
                    return
                elif len(clinic_doctor_nums) == 0:
                    print("该页面无人数板块")
                    cur_page += 1
                    return
                elif int(clinic_doctor_nums[0]) == 0:
                    print("该科室没有人")
                    cur_page += 1
                    return
                elif is_404(html):
                    cur_page += 1
                    return
            except AttributeError:
                return False

            doctor_base_datas = get_doctor_base_info_from_clinic(html)
            doctor_img_datas = get_doctor_img_from_clinic(html)

            DoctorBaseInfoOper.add_all(doctor_base_datas)
            DoctorImgOper.add_all(doctor_img_datas)

            cur_page += 1

def crawl_active_doctor_base_info():
    '''
    通过【根据科室找医生】抓取活跃的医生基本信息和头像信息
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

        doctor_base_info_datas = get_active_doctor_base_info(html)
        doctor_img_datas = get_active_doctor_img(html)

        DoctorBaseInfoOper.add_all(doctor_base_info_datas)
        DoctorImgOper.add_all(doctor_img_datas)

        cur_page += 1

# TODO 抓取所有医生详情页信息（认证信息、标签信息、服务信息、价格信息、简介信息、好评信息、心意墙信息）
#  1.遍历所有医院 2.遍历医院的所有科室 3.获取科室的所有医生id 4.根据id format url并抓取详情页信息
def crawl_all_doctor_detail_info():
    pass

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
            print("开始抓取", doctor_id, "的详情页")
            # crawl_doctor_auth_info(doctor_id)
            # crawl_doctor_tag(doctor_id)
            # crawl_doctor_service_info(doctor_id)
            # crawl_doctor_price(doctor_id)
            # crawl_doctor_description(doctor_id)
            crawl_doctor_comment_label(doctor_id)
            # TODO 完善抓取病情页方法
            # illness_info_datas = crawl_illness_question()
            # crawl_doctor_reward(doctor_id)
            print("抓取完毕")
        # TODO 增加发生错误，存储该doctor_id用于稍后重新抓取

        cur_page += 1


def crawl_doctor_detail_info(doctor_id):
    '''
    通过【医生个人详情页】抓取所有详情信息
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)

    crawl_doctor_auth_info(doctor_id)
    crawl_doctor_tag(doctor_id)
    crawl_doctor_service_info(doctor_id)
    crawl_doctor_price(doctor_id)
    crawl_doctor_description(doctor_id)
    crawl_doctor_comment_label(doctor_id)
    # TODO 完善抓取病情页方法
    # illness_info_datas = crawl_illness_question()
    crawl_doctor_reward(doctor_id)


def crawl_doctor_base_info(doctor_id):
    '''
    crawl doctor base info：抓取医生基本信息
    :param doctor_id:
    :return: doctor base info data
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_base_info = get_doctor_base_info(doctor_id, html)

    # 不存在这个医生
    if not doctor_base_info:
        # 日志警告
        return

    # 该医生不存在表
    if not DoctorBaseInfoOper.get_doctor_base_info_by_doctor_id(doctor_id):
        # 插入日志：新增
        DoctorBaseInfoOper.add_one(doctor_base_info)
    else:
        # 日志：已存在并更新
        DoctorBaseInfoOper.add_one(doctor_base_info)

def crawl_doctor_auth_info(doctor_id):
    '''
    crawl doctor auth info：抓取医生认证信息
    :param doctor_id:
    :return: doctor auth info 对象
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_auth_data = get_doctor_auth_info(doctor_id, html)
    # 不存在这个认证信息
    if not doctor_auth_data:
        # 日志警告
        return

    if not DoctorAuthInfoOper.get_doctor_auth_info_by_doctor_id(doctor_id):
        # 插入日志：新增
        DoctorAuthInfoOper.add_one(doctor_auth_data)
    else:
        # 日志：已存在并更新
        DoctorAuthInfoOper.add_one(doctor_auth_data)

def crawl_doctor_tag(doctor_id):
    '''
    抓取医生标签信息（id、tag【JSON形式存储】）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_tag_data = get_doctor_tag(doctor_id, html)
    # 不存在
    if not doctor_tag_data:
        # 日志警告
        return

    if not DoctorTagOper.get_doctor_tag_by_doctor_id(doctor_id):
        # 插入日志：新增
        print("插入doctor_tag_data")
        DoctorTagOper.add_one(doctor_tag_data)
    else:
        # 日志：已存在并更新
        DoctorTagOper.add_one(doctor_tag_data)

def crawl_doctor_service_info(doctor_id):
    '''
    抓取医生服务信息（id、服务人次、好评率、同行认可、患者心意、关注人数）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_service_data = get_doctor_service_info(doctor_id, html)

    # 不存在
    if not doctor_service_data:
        # 日志警告
        return

    if not DoctorServiceInfoOper.get_doctor_service_info_by_doctor_id(doctor_id):
        # 插入日志：新增
        print("插入doctor_service_data")
        DoctorServiceInfoOper.add_one(doctor_service_data)
    else:
        # 日志：已存在并更新
        DoctorServiceInfoOper.add_one(doctor_service_data)


def crawl_doctor_price(doctor_id):
    '''
    抓取医生价格信息（id、价格、折扣【需判断有无】、类型）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_price_data = get_doctor_price(doctor_id, html)

    # 不存在
    if not doctor_price_data:
        # 日志警告
        return

    if not DoctorPriceOper.get_doctor_price_by_doctor_id(doctor_id):
        # 插入日志：新增
        DoctorPriceOper.add_one(doctor_price_data)
    else:
        # 日志：已存在并更新
        DoctorPriceOper.add_one(doctor_price_data)

def crawl_doctor_description(doctor_id):
    '''
    抓取医生个人简介信息（id、教育背景、专业擅长、个人简介、医院地点）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_description_data = get_doctor_description(doctor_id, html)

    # 不存在
    if not doctor_description_data:
        # 日志警告
        return

    if not DoctorDescriptionOper.get_doctor_description_by_doctor_id(doctor_id):
        # 插入日志：新增
        DoctorDescriptionOper.add_one(doctor_description_data)
    else:
        # 日志：已存在并更新
        DoctorDescriptionOper.add_one(doctor_description_data)

def crawl_doctor_comment_label(doctor_id):
    '''
    抓取医生患者评价标签（id、4个评价标签的数量）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_comment_label_data = get_doctor_comment_label(doctor_id, html)
    # 不存在
    if not doctor_comment_label_data:
        # 日志警告
        return

    if not DoctorCommentLabelOper.get_doctor_comment_label_by_doctor_id(doctor_id):
        # 插入日志：新增
        DoctorCommentLabelOper.add_one(doctor_comment_label_data)
    else:
        # 日志：已存在并更新
        DoctorCommentLabelOper.add_one(doctor_comment_label_data)


def crawl_illness_question(doctor_id):
    '''
    TODO 抓取医生好评问题信息（dr_id、ques_id、clinic_id、type、time、title、detail_html）
    （通过ajax请求抓取）
    :param doctor_id:
    :return:
    '''
    # 1.通过ajax的json获取【所有问题类型列表】
    # 2.遍历不同类型的ajax请求并翻页（翻页需要判断 1.是否返回的json对象为空 2.是否返回的问题数量<20 ）
    # 3.data的不同属性抓取在json中和detail_url中

    pass


def crawl_doctor_reward(doctor_id):
    '''
    抓取医生心意墙信息（id、打赏时间、打赏金额、打赏留言）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    doctor_reward_data = get_doctor_reward(doctor_id, html)
    # 不存在
    if not doctor_reward_data:
        # 日志警告
        return

    if not DoctorRewardOper.get_doctor_reward_by_doctor_id(doctor_id):
        # 插入日志：新增
        DoctorRewardOper.add_all(doctor_reward_data)
    else:
        # 日志：已存在并更新
        DoctorRewardOper.add_all(doctor_reward_data)


if __name__ == '__main__':
    # crawl_active_doctor_base_info()
    # crawl_active_doctor_detail_info()
    crawl_all_doctor_base_info()