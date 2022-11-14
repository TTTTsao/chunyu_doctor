import re

from bs4 import BeautifulSoup
from lxml import etree

from spider.page_get.clinic_basic import get_clinic_html

BASE_URL = 'https://chunyuyisheng.com/pc/doctors/0-0-0/'
CLINIC_URL = 'https://chunyuyisheng.com/pc/doctors/{}/'

def get_first_clinic_id_list(html):
    '''
    get the list of first clinics' ids
    used for crawl second clinics
    :param html:
    :return: first clinic ids list
    '''
    soup = BeautifulSoup(html, 'html.parser')
    first_clinic_row_list = soup.find_all("li", class_='tab-item')
    first_clinic_id_list = []

    # 使用正则将其余id提取出来并存入新列表
    for item in first_clinic_row_list:

        pattern = re.compile("\S{12}")
        data = re.sub(pattern, '', item.contents[1]['href'])
        data = re.sub("/$", '', data)

        first_clinic_id_list.append(data)

    del first_clinic_id_list[0]
    del first_clinic_id_list[len(first_clinic_id_list)-1]

    return first_clinic_id_list

def get_first_clinic_list(html):
    '''
    get the list of first clinic info (id and name)
    :param html:
    :return: first clinic info list (id and name)
    '''
    soup = BeautifulSoup(html, 'html.parser')
    first_clinic_row_list = soup.find_all("li", class_='tab-item')
    first_clinic_list = []

    # 将id与name以列表形式存入列表
    for item in first_clinic_row_list:
        temp_list = []

        # get id data
        pattern = re.compile("\S{12}")
        id_data = re.sub(pattern, '', item.contents[1]['href'])
        id_data = re.sub("/$", '', id_data)
        temp_list.append(id_data)

        # get name data
        pattern = '(\S+)'
        name_data = re.search(pattern, item.contents[1].string).group()
        temp_list.append(name_data)

        first_clinic_list.append(temp_list)

    del first_clinic_list[0]
    del first_clinic_list[len(first_clinic_list)-1]
    return first_clinic_list

def get_second_clinic_list(first_clinic_id_list):
    '''
    get second clinic info
    :param first_clinic_id_list:
    :return: second clinic info list (first_id, second_id and name)
    '''
    second_clinic_list = []

    for first_clinic_id in first_clinic_id_list:
        flag = is_second_clinic_exist(first_clinic_id)
        if flag:
            second_clinic_list.append(flag)
        else:
            print('===无二级科室===',first_clinic_id)
            continue

    print(second_clinic_list)
    return second_clinic_list


def is_second_clinic_exist(first_clinic_id):
    '''
    if second clinic exist
    :param first_clinic_id:
    :return: data_list
    '''
    url = CLINIC_URL.format(first_clinic_id)
    html = get_clinic_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    ul_data = soup.find_all("ul", class_='tab-type-free')

    # 判断是否存在除了【全部科室】之外的二级科室，并抓取
    count = 0
    data_list = []
    for ul in ul_data:
        for li in ul.find_all('li'):
            temp_list = []
            # get second_clinic_id
            pattern = re.compile("\S{12}")
            id_data = re.sub(pattern, '', li.contents[1]['href'])
            id_data = re.sub("/$", '', id_data)

            # get second_clinic_name
            pattern = '(\S+)'
            name_data = re.search(pattern, li.contents[1].string).group()

            temp_list.append(first_clinic_id)
            temp_list.append(id_data)
            temp_list.append(name_data)
            count = count+1
            data_list.append(temp_list)

    if count > 1 :
        # delete all_clinic and return data_list
        del data_list[0]
        return data_list
    else:
        return False


if __name__ == '__main__':
    html = get_clinic_html(BASE_URL)
    first_clinic_list = get_first_clinic_id_list(html)
    # print("first_clinic_list",first_clinic_list)
    # string = '0-0-2'
    # print(get_second_clinic_list(first_clinic_list))