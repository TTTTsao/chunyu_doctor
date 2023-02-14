import json
from lxml import etree
from bs4 import BeautifulSoup
from spider.page_get.basic import get_page_html
from spider.db.models import IllnessInfo
from spider.util.basic import trans_to_datetime
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import is_illness_detail_page_right
from loguru import logger

ILLNESS_DETAIL_URL = 'https://www.chunyuyisheng.com/pc/qa/{}'

@parse_decorator(False)
def get_illness_datas(doctor_id, type_item, html):
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
        illness_data.illness_type = type_item
        illness_data.illness_question_id = problem["id"]

        # TODO 判断question是否已经被抓取和完整录入

        illness_data.illness_title = problem["title"]
        illness_data.illness_time = trans_to_datetime(problem["date_str"])
        illness_data.clinic_id = get_illness_clinic_id(illness_data.illness_question_id)
        illness_data.illness_detail_html = get_illness_html(illness_data.illness_question_id)

        illness_datas.append(illness_data)
    return illness_datas

@parse_decorator(False)
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

@parse_decorator(False)
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

@parse_decorator(False)
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

@parse_decorator(False)
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
        return ''
    except AttributeError:
        return ''
    return clinic_id

@parse_decorator(False)
def get_illness_html(question_id):
    '''
    从ajaz页获取illness html
    :param illness_question_id:
    :return:
    '''
    url = ILLNESS_DETAIL_URL.format(question_id)
    html = get_page_html(url)
    if not is_illness_detail_page_right(question_id, html):
        logger.error("被反爬，{} 问诊对话详情页面与对应医生不一致".format(question_id))
        return False
    soup = BeautifulSoup(html, 'html.parser')
    try:
        logger.info("抓取 {} 病情详情页".format(question_id))
        illness_row_html = str(soup.find_all(attrs={'class': 'context-left'}))
        illness_html = illness_row_html.replace("\t", '').replace("\n", '').replace(" ", '')
    except Exception:
        return False
    return illness_html

def is_cont_not_none(cont):
    if (cont is None):
        return False
    else:
        return True
