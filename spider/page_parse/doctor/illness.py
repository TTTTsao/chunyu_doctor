import json
from lxml import etree
from bs4 import BeautifulSoup
from spider.page_get.basic import get_page_html
from spider.db.models import IllnessInfo
from spider.util.basic import trans_to_datetime

ILLNESS_DETAIL_URL = 'https://www.chunyuyisheng.com/pc/qa/{}'

def get_illness_datas(doctor_id, type, html):
    '''
    从ajax页抓取illness信息
    :param html:
    :return:
    '''
    if not html:
        return

    illness_datas = []
    problem_list = get_illness_problem_list(html)
    for problem in problem_list:
        illness_data = IllnessInfo()
        illness_data.doctor_id = doctor_id
        illness_data.illness_type = type
        illness_data.illness_question_id = problem["id"]
        illness_data.illness_title = problem["title"]
        illness_data.illness_time = trans_to_datetime(problem["date_str"])
        illness_data.clinic_id = get_illness_clinic_id(illness_data.illness_question_id)
        illness_data.illness_detail_html = get_illness_html(illness_data.illness_question_id)

        illness_datas.append(illness_data)
    return illness_datas

def get_illness_hot_consults(html):
    '''
    从ajax页获取illness hot consults
    :param html:
    :return:
    '''
    if not html:
        return
    cont = json.loads(html).get('hot_consults')
    hot_consults = []
    for item in cont:
        hot_consults.append(item["keywords"])
    return hot_consults

def get_illness_problem_list(html):
    '''
    从ajax页获取illness problem list
    :param html:
    :return:
    '''
    if not html:
        return
    cont = json.loads(html).get('problem_list')
    return cont


def is_illness_none(html):
    if not html:
        return
    cont = json.loads(html).get('hot_consults')
    print(cont)
    print(type(cont))
    print(cont is None)
    if (cont is None):
        print("cont's type is NoneType")
        return False
    return True if (len(cont) == 0) else False

def has_more_page(html):
    if not html:
        return
    cont = json.loads(html).get("has_more_page")
    return cont

def get_illness_clinic_id(question_id):
    '''
    从ajax页获取illness clinic id
    :param question_id:
    :return:
    '''
    url = ILLNESS_DETAIL_URL.format(question_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)
    try:
        clinic_id = xpath.xpath("//div[@class='bread-crumb-spacial']/a/text()")[0]
    except IndexError: return
    except AttributeError: return
    return clinic_id

def get_illness_html(question_id):
    '''
    从ajaz页获取illness html
    :param illness_question_id:
    :return:
    '''
    url = ILLNESS_DETAIL_URL.format(question_id)
    html = get_page_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        illness_html = str(soup.find_all(attrs={'class': 'problem-detail-wrap'}))
    except:
        print("illness html goes wrong")
        return
    return illness_html

if __name__ == '__main__':
    url = 'https://www.chunyuyisheng.com/pc/doctor/clinic_web_d675c6211d0f2900/qa/?is_json=1&tag=&page_count=20&page=1'
    html = get_page_html(url)
    is_illness_none(html)