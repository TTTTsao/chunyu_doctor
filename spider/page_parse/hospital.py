import re
import json
import datetime

from bs4 import BeautifulSoup
from lxml import etree

from spider.page_get.basic import get_page_html

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

def get_clinic_rank(hospital_id):
    '''
    get clinic rank info from hospital detail page
    :param hospital_id:
    :return: clinic rank info data
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    row_rank_data_list = xpath.xpath('/html/body/div[4]/div[3]/ul/li/a/text()')
    rank_name_list = []
    rank_level_list = []

    for i in range(len(row_rank_data_list)):
        rank_name = get_reg_rank_name(str(row_rank_data_list[i]))
        rank_level = get_reg_rank_level(str(row_rank_data_list[i]))
        rank_name_list.append(rank_name)
        rank_level_list.append(rank_level)
        #TODO 写入 clinic rank info 对象

    # TODO 返回 clinic rank info 对象
    return ''

def get_hospital_clinic_base_info(clinic_id):
    '''
    get hospital's clinic base info from clinic detail page
    :param clinic_id:
    :return: hospital_clinic_base_info data
    '''

    url = HOSPITAL_CLINIC_URL.format(clinic_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    id = clinic_id
    clinic_name = str(xpath.xpath('/html/body/div[4]/div[1]/h3/text()'))
    clinic_profile = '无'

    row_profile = xpath.xpath('/html/body/div[4]/div[3]/div/p/text()')
    # 判断没有科室简介的情况
    if len(row_profile) != 0:
        clinic_profile = get_reg_clinic_profile(str(row_profile))

    # TODO 写入 hospital_clinic_base_info 对象


    # TODO 返回 hospital_clinic_base_info 对象
    return ''


def get_hospital_realtime_inquiry_nums(hospital_id):
    '''
    get hospital realtime inquiry doctors nums info from detail page
    :param hospital_id:
    :return: hospital_realtime_inquiry_nums data
    '''

    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    id = hospital_id
    inquiry_nums = xpath.xpath('/html/body/div[4]/div[4]/span[3]/text()')[0]

    # TODO 返回 hospital_realtime_inquiry_nums data 对象
    return ''


def get_hospital_enter_doctor_info(hospital_id):
    '''
    get hospital enter doctor info from detail page
    :param hospital_id:
    :return: hospital_enter_doctor_info data
    '''
    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    hospital_id = hospital_id
    clinic_id_list = []
    enter_nums_list = []

    row_clinic_id_list = xpath.xpath('//*[@id="clinic"]/li/a/@href')
    row_enter_nums_list = xpath.xpath('//*[@id="clinic"]/li/span/i/text()')

    # 判断该科室是否为0人，如果是0人需要返回0
    for i in range(len(row_clinic_id_list)):
        if len(row_clinic_id_list) > len(row_enter_nums_list):
            if ( i - len(row_enter_nums_list) ) > -1:
                clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
                clinic_id_list.append(clinic_id)
                enter_nums_list.append(0)
            else:
                clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
                clinic_id_list.append(clinic_id)
                enter_nums_list.append(int(row_enter_nums_list[i]))
        else:
            clinic_id = get_reg_clinic_id(str(row_clinic_id_list[i]))
            clinic_id_list.append(clinic_id)
            enter_nums_list.append(int(row_enter_nums_list[i]))
    # print(clinic_id_list)
    # print(enter_nums_list)
    # TODO 返回 hospital_enter_doctor_info data 对象
    return ''

def get_hospital_base_info(hospital_id):
    '''
    get hospital base info from detail page
    :param html:
    :return: hospital_base_info data
    '''

    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    id = hospital_id
    name = (xpath.xpath('/html/body/div[4]/ul[1]/li[4]/text()'))[0]
    area = (xpath.xpath('//*[@id="region_href"]/text()'))[0]
    province = (xpath.xpath('/html/body/div[4]/ul[1]/li[3]/a/text()'))[0]

    city = ''
    temp_city = xpath.xpath('/html/body/div[4]/ul[1]/li[4]/a/text')
    if len(temp_city) == 0:
        city = ''
    else:
        city = temp_city[0]

    row_profile = xpath.xpath('/html/body/div[4]/div[3]/div[1]/p/text()')
    str_profile = str(row_profile)
    profile = get_reg_hospital_profile(str_profile)

    # JSON-tag
    tag_dic = {}
    tag_dic["rank"] = xpath.xpath("/html/body/div[4]/div[1]/span[1]/text()")[0]
    tag_dic["type"] = xpath.xpath("/html/body/div[4]/div[1]/span[2]/text()")[0]
    tag = json.dumps(tag_dic, ensure_ascii=False)  # ensure_ascii=False 防止中文被转化

    # TODO 返回 hospital_base_info 对象
    return ''


def get_hospital_list_from_province(province_id):
    '''
    get hospital id list by province
    :param province_id_list:
    :return: hospital list (id and city)
    '''

    url = HOSPITAL_URL.format(province_id)
    html = get_page_html(url)
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


def get_reg_clinic_rank_id(str):
    '''
    use re to get clinic rank id
    :param str:
    :return: clinc_rank_id
    '''
    pattern = '/pc/hospitallist/0/'
    clinc_rank_id = re.sub(pattern, '', str)
    return clinc_rank_id

def get_reg_clinic_name(str):
    '''
    use re to get clinic name
    :param str:
    :return:
    '''
    pattern = '([\u4e00-\u9fa5]+)'
    clinic_name = re.search(pattern, str).group()
    return clinic_name

def get_reg_province_id(str):
    '''
    use re to get province id
    :param str:
    :return: province id
    '''
    pattern = '([\d+]+-[\d])'
    province_id = re.search(pattern, str).group()
    return province_id

def get_reg_hospital_id(str):
    '''
    use re to get hospital id
    :param str:
    :return: hospital id
    '''
    pattern = re.compile("/pc/hospital/")
    id_data = re.sub(pattern, '', str)
    hospital_id = re.sub("/$", '', id_data)
    return hospital_id

def get_reg_hospital_profile(str):
    '''
    use re to get hospital profile
    :param str:
    :return: hospital profile
    '''
    front_pattern = re.compile("^[\S{10}]+[\s*]+[\S*]+[\s*]+[\S*]+[\s*]+[\s*]")
    front_reg = re.sub(front_pattern, '', str)
    mid_pattern = re.compile('[\']+[,]+[\s]+[\']+[\\\\]+[u3000]+[\\\\]+[u3000]+[\d]*')
    mid_reg = re.sub(mid_pattern, '', front_reg)
    end_pattern = re.compile("\\\\+n+[\s*]+[\S*]+']$")
    end_reg = re.sub(end_pattern, '', mid_reg)
    return end_reg

def get_reg_clinic_id(str):
    '''
    use re to get clinic id
    :param str:
    :return: clinic id
    '''
    pattern = re.compile("/pc/clinic/")
    id_data = re.sub(pattern, '', str)
    clinic_id = re.sub("/$", '', id_data)
    return clinic_id

def get_reg_rank_name(str):
    '''
    use re to get rank name
    :param str:
    :return: rank name
    '''
    pattern = re.compile('[排名第]+[\d]*$')
    rank_name = re.sub(pattern, '', str)
    return rank_name

def get_reg_rank_level(str):
    '''
    use re to get rank level
    :param str:
    :return: rank level(int)
    '''
    rank_level = int(re.search('(\d)*$', str).group())
    return rank_level

def get_reg_clinic_profile(str):
    '''
    use re to get clinic profile
    :param str:
    :return: clinic profile
    '''
    front_pattern = re.compile("^[\S{10}]+[\s*]+[\S*]+[\s]*")
    front_reg = re.sub(front_pattern, '', str)
    mid_pattern = re.compile('[\']+[,]+[\s]+[\']+[\\\\]+[u3000]+[\\\\]+[u3000]+[\d]*')
    mid_reg = re.sub(mid_pattern, '', front_reg)
    end_pattern = re.compile("\\\\+n+[\s*]+[\S*]+']$")
    end_reg = re.sub(end_pattern, '', mid_reg)
    return end_reg

def get_datetime():
    time_now = datetime.datetime.today()
    return time_now

if __name__ == '__main__':
    # html = get_page_html(BASE_URL)
    # get_hospital_province_list(html)
    # str = '/pc/hospital/040093b0ca34328b/'
    # print(str)
    # print(get_reg_hospital_id(str))
    hospital_id = '3c7328db652e8dc0'
    row_clinic_id = '/pc/clinic/00245b9d266dac6d-ab/'
    row_rank = '全国综合排名第36'
    hospital_clinic_id = '3c7328db652e8dc0-bj'
    first_id = '/pc/hospitallist/0/fa/'
    clinic_name = '\n            预防保健科\n          '
    clinc_id = '/pc/hospitallist/0/mb'
    print(get_reg_clinic_rank_id(clinc_id))
    # is_second_clinic_exist(first_id)
    # get_reg_clinic_name(clinic_name)
    # get_hospital_clinic_base_info(hospital_clinic_id)
    # print(get_reg_rank_level(row_rank))
    # get_hospital_base_info(hospital_id)
    # get_reg_hospital_profile(str)
    # print(get_hospital_enter_doctor_info(hospital_id))
    # get_hospital_enter_doctor_info(hospital_id)
    # print(get_reg_clinic_id(row_clinic_id))
    # get_clinic_format_url_list()


