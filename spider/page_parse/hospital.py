import json

from bs4 import BeautifulSoup
from lxml import etree

from spider.page_get.basic import get_page_html
from spider.util.reg.reg_hospital import *
from spider.db.models import *

BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_RANK_URL = 'https://chunyuyisheng.com//pc/hospitallist/{}/{}'

def get_hospital_rank(location_id, clinic_id, is_second_page = False):
    '''

    :param location_id:
    :param clinic_id:
    :param is_second_page:
    :return: hospital_rank info data
    '''
    url = HOSPITAL_CLINIC_URL.format(location_id, clinic_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    area = str(xpath.xpath('/html/body/div[4]/section[1]/div[1]/ul/li[2]/a/text()'))
    province = str(xpath.xpath('/html/body/div[4]/section[1]/div[1]/ul/li[3]/a/text()'))
    # TODO 判断province是否为空
    city = str(xpath.xpath('/html/body/div[4]/section[1]/div[1]/ul/li[4]/a/text()'))
    # TODO 判断city是否为空

    # TODO 选取当前selected的一级科室

    # TODO 判断是否为二级科室排名页面

    # TODO 写入 hospital rank info data 对象

    # TODO 返回 hospital rank info data 对象

    pass

def get_hospital_clinic_rank(hospital_id, html):
    '''
    get clinic rank info from hospital detail page
    :param hospital_id:
    :return: clinic rank info data
    '''
    if not html:
        return

    xpath = etree.HTML(html)
    hospital_clinic_rank_datas = []
    row_rank_data_list = xpath.xpath("//li[@class='hospital-rank']/a/text()")
    print(row_rank_data_list)

    # 判断是否存在排名信息
    if len(row_rank_data_list) == 0:
        print("无医院排名信息")
        return

    for i in range(len(row_rank_data_list)):
        hospital_clinic_rank = HospitalClinicRank()
        hospital_clinic_rank.hospital_id = hospital_id
        hospital_clinic_rank.rank_name = get_reg_rank_name(str(row_rank_data_list[i]))
        hospital_clinic_rank.rank_level = get_reg_rank_level(str(row_rank_data_list[i]))
        hospital_clinic_rank_datas.append(hospital_clinic_rank)

    return hospital_clinic_rank_datas

def get_hospital_clinic_base_info(clinic_id, html):
    '''
    get hospital's clinic base info from clinic detail page
    :param clinic_id:
    :return: hospital_clinic_base_info data
    '''
    if not html:
        return
    xpath = etree.HTML(html)
    hospital_clinic_data = HospitalClinicBaseInfo()

    hospital_clinic_data.hospital_clinic_id = clinic_id
    hospital_clinic_data.hospital_clinic_name = str(xpath.xpath('/html/body/div[4]/div[1]/h3/text()')[0])

    row_profile = xpath.xpath('/html/body/div[4]/div[3]/div/p/text()')
    # 没有科室简介
    if len(row_profile) != 0:
        hospital_clinic_data.hospital_clinic_profile = get_reg_clinic_profile(str(row_profile))

    return hospital_clinic_data


def get_hospital_real_time_inquiry(hospital_id, html):
    '''
    get hospital realtime inquiry doctors nums info from detail page
    :param hospital_id:
    :return: hospital_realtime_inquiry_nums data
    '''
    if not html:
        return
    hospital_real_time_inquiry_data = HospitalRealTimeInquiry()
    xpath = etree.HTML(html)

    hospital_real_time_inquiry_data.hospital_id = hospital_id

    # TODO 1.将该错误记录于日志 2.记录该hospital_id用于后续重新尝试爬取
    try:
        inquiry_nums = xpath.xpath("//span[@class='light'][2]/text()")[0]
        print("inquiry_nums", inquiry_nums)
        hospital_real_time_inquiry_data.real_time_inquiry_doctor_num = int(inquiry_nums)
    except:
        hospital_real_time_inquiry_data.real_time_inquiry_doctor_num = 0

    return hospital_real_time_inquiry_data


def get_hospital_enter_doctor_info(hospital_id, html):
    '''
    get hospital enter doctor info from detail page
    :param hospital_id:
    :return: hospital_enter_doctor_info data
    '''
    if not html:
        return
    xpath = etree.HTML(html)
    hospital_enter_datas = []

    # 判断页面科室暂无的情况
    try:
        if '暂无相关信息' in html:
            # 日志记录
            print("暂无相关信息")
            return False
    except AttributeError:
        return False

    row_clinic_id_list = xpath.xpath('//*[@id="clinic"]/li/a/@href')
    row_enter_nums_list = xpath.xpath('//*[@id="clinic"]/li/span/i/text()')


    # 判断该科室是否为0人，如果是0人需要返回0
    for i in range(len(row_clinic_id_list)):
        hospital_enter_data = HospitalClinicEnterDoctor()
        hospital_enter_data.hospital_id = hospital_id
        hospital_enter_data.hospital_clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
        if len(row_clinic_id_list) > len(row_enter_nums_list):
            # 有科室为0人
            if ( i - len(row_enter_nums_list) ) > -1:
                # 进入为0人的科室
                hospital_enter_data.hospital_clinic_amount = 0
            else:
                hospital_enter_data.hospital_clinic_amount = int(row_enter_nums_list[i])
        else:
            hospital_enter_data.hospital_clinic_amount = int(row_enter_nums_list[i])

        hospital_enter_datas.append(hospital_enter_data)

    return hospital_enter_datas

def get_hospital_base_info(hospital_id, city, html):
    '''
    get hospital base info from detail page
    :param html:
    :return: hospital_base_info data
    '''
    if not html:
        return
    hospital_data = Hospital()
    xpath = etree.HTML(html)

    hospital_data.hospital_id = hospital_id
    hospital_data.hospital_city = city
    name = (xpath.xpath('/html/body/div[4]/div[1]/h3/text()'))[0]
    hospital_data.hospital_name = str(name)

    area = (xpath.xpath('//*[@id="region_href"]/text()'))[0]
    hospital_data.hospital_area = str(area)

    province = (xpath.xpath('/html/body/div[4]/ul[1]/li[3]/a/text()'))[0]
    hospital_data.hospital_province = str(province)

    # temp_city = xpath.xpath('/html/body/div[4]/ul[1]/li[4]/a/text')
    # if len(temp_city) != 0:
    #     hospital_data.hospital_city = str(temp_city[0])

    row_profile = xpath.xpath("//div[@class='content-info']/div[1]/p/text()")
    str_profile = str(row_profile)
    hospital_data.hospital_profile = get_reg_hospital_profile(str_profile)

    # JSON-tag
    tag_dic = {}
    tag_dic["rank"] = xpath.xpath("/html/body/div[4]/div[1]/span[1]/text()")[0]
    tag_dic["type"] = xpath.xpath("/html/body/div[4]/div[1]/span[2]/text()")[0]
    hospital_data.hospital_tag = json.dumps(tag_dic, ensure_ascii=False)  # ensure_ascii=False 防止中文被转化

    return hospital_data


def get_hospital_list_from_province(html):
    '''
    get hospital id list by province
    :param province_id_list:
    :return: hospital list (id and city)
    '''
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')
    div_data = soup.find_all(class_='list')

    hospital_list = []

    for item in div_data:
        city = item.find(name="label").string
        for li in item.find_all("li"):
            temp_list = []
            str = li.contents[1]['href']
            hospital_id = get_reg_hospital_id(str)
            temp_list.append(hospital_id)
            temp_list.append(city)
            hospital_list.append(temp_list)
    return hospital_list


def get_hospital_province_list(html):
    '''
    get province id list of hospital
    :param html:
    :return: province id list
    '''
    if not html:
        return
    soup = BeautifulSoup(html, 'html.parser')
    ul_data = soup.find_all("ul", class_='city')

    province_id_list = []

    for ul in ul_data:
        for li in ul.find_all('li'):
            province_id = get_reg_province_id(li.contents[0]['href'])
            province_id_list.append(province_id)
    print(province_id_list)
    return province_id_list

# 获取排名信息处一级科室id和二级科室id，并置于同一个list返回 [ {1st_id, 1st_name}, [list 2nd: {2nd_id, 2nd_name}] ]
def get_clinic_format_url_list():
    '''
    get clinic id list
    use to get rank info
    :return: list [ [ {1st_id, 1st_name}, [list 2nd: {2nd_id, 2nd_name}] ]
    '''
    html = get_page_html(HOSPITAL_RANK_URL.format('0', '0'))
    xpath = etree.HTML(html)

    clinic_format_url_list = []

    row_first_id_list = xpath.xpath('/html/body/div[4]/section[1]/div[2]/div[2]/div/select/option/@value')
    row_first_name_list = xpath.xpath('/html/body/div[4]/section[1]/div[2]/div[2]/div/select/option/text()')

    # print("==len(row_first_id_list)==", len(row_first_id_list))

    for i in range(len(row_first_id_list)):
        # print('==i==', i)
        first_dic = {}
        first_id = str(row_first_id_list[i])
        first_dic["first_id"] = first_id
        first_name = get_reg_clinic_name(str(row_first_name_list[i]))
        first_dic["first_name"] = first_name
        # print('==first_id==', first_id, '==first_name==', first_name)

        # 判断是否有二级id
        second_dic_list = is_second_clinic_exist(first_id)
        if not second_dic_list:
            # 没有二级科室
            second_dic_list = []

        # print('==second_dic_list==', second_dic_list)
        temp_list = []
        temp_list.append(first_dic)
        temp_list.append(second_dic_list)
        clinic_format_url_list.append(temp_list)
        # print('==clinic_format_url_list==', clinic_format_url_list)

    # print(clinic_format_url_list)

    return clinic_format_url_list

def is_second_clinic_exist(first_id):
    '''
    whether second_clinic_exist
    :param first_id:
    :return: second_dic_list [ {1sec_id, 1sec_name}, {2sec_id, 2sec_name}, ... ]
    '''
    html = get_page_html(HOSPITAL_RANK_URL.format(first_id))
    xpath = etree.HTML(html)

    row_second_id_list = xpath.xpath('/html/body/div[4]/section[1]/div[2]/div[2]/div/select[2]/option/@value')
    row_second_name_list = xpath.xpath('/html/body/div[4]/section[1]/div[2]/div[2]/div/select[2]/option/text()')
    second_dic_list = []

    if len(row_second_id_list) == 0:
        return False
    else:
        for i in range(len(row_second_name_list)):
            # print('==i==', i)
            second_dic = {}
            second_id = str(row_second_id_list[i])
            second_dic['second_id'] = second_id
            # print('==second_id==', second_id)

            second_name = get_reg_clinic_name(str(row_second_name_list[i]))
            second_dic['second_name'] = second_name
            # print("==second_name==", second_name)
            # print('=============================')
            # print(second_dic)

            second_dic_list.append(second_dic)
            # print('==second_dic_list==', second_dic_list)
        return second_dic_list


def get_clinic_id_list(html):
    '''
    get clinic id list from hospital detail list
    :param html:
    :return:
    '''
    if not html:
        return
    # 判断页面科室暂无的情况
    try:
        if '暂无相关信息' in html:
            # 日志记录
            print("暂无相关信息")
            return False
    except AttributeError:
        return False

    xpath = etree.HTML(html)
    row_clinic_id_list = xpath.xpath('//*[@id="clinic"]/li/a/@href')
    clinic_id_list = []
    # 循环遍历获取科室id
    for i in range(len(row_clinic_id_list)):
        clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
        clinic_id_list.append(clinic_id)

    return clinic_id_list



if __name__ == '__main__':
    # base_url = 'https://chunyuyisheng.com/pc/hospital/a954126543a7ba9d/'
    # hospital_id = 'a954126543a7ba9d'
    # city = '唐山市'
    # base_url = 'https://chunyuyisheng.com/pc/hospitals/'
    url = 'https://chunyuyisheng.com/pc/hospital/00245b9d266dac6d/'
    html = get_page_html(url)
    hospital_id = '00245b9d266dac6d'
    get_hospital_clinic_rank(hospital_id, html)





