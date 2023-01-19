from bs4 import BeautifulSoup
from lxml import etree

from spider.page_get.basic import get_page_html
from spider.util.reg.reg_hospital import (get_reg_hospital_id, get_reg_province_id,
                                          get_reg_clinic_name, get_reg_clinic_id)

HOSPITAL_RANK_URL = 'https://chunyuyisheng.com//pc/hospitallist/{}/{}'

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

    for i in range(len(row_first_id_list)):
        first_dic = {}
        first_id = str(row_first_id_list[i])
        first_dic["first_id"] = first_id
        first_name = get_reg_clinic_name(str(row_first_name_list[i]))
        first_dic["first_name"] = first_name

        # 判断是否有二级id
        second_dic_list = is_second_clinic_exist(first_id)
        if not second_dic_list:
            # 没有二级科室
            second_dic_list = []

        temp_list = []
        temp_list.append(first_dic)
        temp_list.append(second_dic_list)
        clinic_format_url_list.append(temp_list)

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
            second_dic = {}
            second_id = str(row_second_id_list[i])
            second_dic['second_id'] = second_id

            second_name = get_reg_clinic_name(str(row_second_name_list[i]))
            second_dic['second_name'] = second_name

            second_dic_list.append(second_dic)
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