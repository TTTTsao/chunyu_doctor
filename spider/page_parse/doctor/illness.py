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
    if not problem_list:
        return
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
    if is_cont_not_none(cont):
        hot_consults = []
        for item in cont:
            hot_consults.append(item["keywords"])
        return hot_consults
    else:
        return False


def get_illness_problem_list(html):
    '''
    从ajax页获取illness problem list
    :param html:
    :return:
    '''
    if not html:
        return
    cont = json.loads(html).get('problem_list')
    if is_cont_not_none(cont):
        return cont
    else:
        return False


def is_illness_none(html):
    if not html:
        return
    cont = json.loads(html).get('hot_consults')
    if is_cont_not_none(cont):
        return True if (len(cont) == 0) else False
    else:
        return False

def has_more_page(html):
    if not html:
        return
    cont = json.loads(html).get("has_more_page")
    if is_cont_not_none(cont):
        return cont
    else:
        return False

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
    except IndexError:
        # TODO parse-error
        return
    except AttributeError:
        # TODO parse-error
        return
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
        illness_row_html = str(soup.find_all(attrs={'class': 'context-left'}))
        illness_html = illness_row_html.replace("\t", '').replace("\n", '').replace(" ", '')
    except:
        # TODO  parse-warning日志-illness detail html出现问题
        print("illness html goes wrong")
        return
    return illness_html

def is_cont_not_none(cont):
    if (cont is None):
        # TODO parse-warning日志-illness json页无信息（NoneType）
        print("cont's type is NoneType")
        return False
    else:
        return True
