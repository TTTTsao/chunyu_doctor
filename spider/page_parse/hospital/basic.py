from bs4 import BeautifulSoup
from lxml import etree

from spider.page_get.basic import get_page_html
from spider.util.reg.reg_hospital import (get_reg_hospital_id, get_reg_province_id,
                                          get_reg_clinic_name, get_reg_clinic_id)
from spider.decorators.parse_decorator import parse_decorator


HOSPITAL_RANK_URL = 'https://chunyuyisheng.com/pc/hospitallist/{}/{}'

@parse_decorator(False)
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

@parse_decorator(False)
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
    return province_id_list


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
            second_dic = {}
            second_id = str(row_second_id_list[i])
            second_dic['second_id'] = second_id

            second_name = get_reg_clinic_name(str(row_second_name_list[i]))
            second_dic['second_name'] = second_name

            second_dic_list.append(second_dic)
        return second_dic_list

@parse_decorator
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
            return False
    except AttributeError:
        return False

    xpath = etree.HTML(html)
    try:
        row_clinic_id_list = xpath.xpath('//*[@id="clinic"]/li/a/@href')
    except Exception:
        return False
    clinic_id_list = []
    # 循环遍历获取科室id
    for i in range(len(row_clinic_id_list)):
        clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
        clinic_id_list.append(clinic_id)

    return clinic_id_list