
from lxml import etree
from bs4 import BeautifulSoup
from decimal import Decimal
from spider.decorators.parse_decorator import parse_decorator
from spider.db.dao.doctor_dao import (DoctorBaseInfoOper, DoctorIllnessOper)
from spider.util.reg.reg_doctor import get_reg_doctor_id, get_reg_followers, get_reg_mobile_price
from spider.util.log_util import create_parse_logger
logger = create_parse_logger()
logger.remove()



@parse_decorator(False)
def is_404(html):
    try:
        # doctor detail info is deleted
        if '抱歉，你所访问的网页不存在了，请返回主页' in html:
            return True
        elif html == '':
            return True
        else:
            return False
    except AttributeError:
        return False

@parse_decorator(False)
def is_page_has_no_info(html):
    try:
        if '暂无相关信息' in html:
            return True
        else:
            return False
    except AttributeError:
        return False


@parse_decorator(False)
def is_page_has_no_doctor_nums(html, clinic_doctor_nums):
    try:
        if '暂无相关信息' in html:
            logger.warning("该页面暂无医生相关信息")
            return True
        elif len(clinic_doctor_nums) == 0:
            logger.warning("该页面无人数板块")
            return True
        elif int(clinic_doctor_nums[0]) == 0:
            logger.warning("该科室页面人数为0")
            return True
        elif is_404(html):
            return True
    except AttributeError:
        return False


def is_doctor_detail_page_right(doctor_id, html):
    '''
    判断当前 医生pc详情页 是否被反爬
    :param doctor_id:医生id
    :param html:医生pc详情页
    :return:是否被反爬
    '''
    name = DoctorBaseInfoOper.get_doctor_name_by_doctor_id(doctor_id)
    xpath = etree.HTML(html)
    page_name = str(xpath.xpath("//div[@class='doctor-info-item']/div[@class='detail']/div[1]/span[@class='name']/text()")[0])

    if name == page_name:
        return True
    else:
        return False

def is_doctor_mobile_detail_page_right(doctor_id, html):
    '''
    判断当前 医生mobile详情页 是否被反爬
    :param doctor_id:医生id
    :param html:医生mobile详情页
    :return:是否被反爬
    '''
    xpath = etree.HTML(html)
    real_id = str(xpath.xpath("//input[1]/@data-doctor-id")[0])
    if real_id == doctor_id:
        return True
    else:
        return False

def is_illness_detail_page_right(question_id, html):
    '''
    判断当前 问诊对话详情 页面是否被反爬
    :param question_id:
    :param html:
    :return:
    '''
    soup = BeautifulSoup(html, "lxml")
    page_question_id = soup.find(name="div", class_="js-info")["data-problem"]
    if question_id == page_question_id:
        return True
    else:
        return False


def is_price_exist(xpath):
    '''
    判断医生pc详情页的price是否存在
    :param xpath:
    :return: True/False
    '''
    price = xpath.xpath("//a[@class='doctor-pay-wrap']/div[@class='doctor-pay-consult']/span/text()")
    if len(price) == 0:
        return False
    else:
        return True

def is_mobile_price_exist(xpath):
    '''
    判断医生mobile详情页的price是否存在
    :param xpath:
    :return: True/False
    '''
    raw_price = xpath.xpath("//div[@id='referring-physician']/div[2]/div[@class='rp-head']/div/div[1]/text()")[0]
    price = Decimal(get_reg_mobile_price(str(raw_price)))
    if price == -1:
        return False
    elif price > 0:
        return True


def is_service_info_exist(xpath):
    '''
    判断医生详情页的service_info是否存在
    :param xpath:
    :return: True/False
    '''
    try:
        serve_nums = xpath.xpath("//ul[@class='doctor-data']/li[1]/span[1]/text()")[0]
        favorable_rate = xpath.xpath("//ul[@class='doctor-data']/li[2]/span[1]/text()")[0]
        peer_recognization = xpath.xpath("//ul[@class='doctor-data']/li[3]/span[1]/text()")[0]
        patient_praise_num = xpath.xpath("//ul[@class='doctor-data']/li[4]/span[1]/text()")[0]
        followers = xpath.xpath("//div[@class='wexin-qr-code']//div[@class='footer-des']/text()")[0]
    except IndexError:
        return False
    doctor_serve_followers = get_reg_followers(str(followers))

    if str(serve_nums) == '--' and str(favorable_rate) == '--' and str(peer_recognization) == '--' and str(patient_praise_num) == '--'and doctor_serve_followers == 0:
        return False
    else: return True

def is_mobile_service_info_exist(xpath):
    '''
    判断医生mobile详情页的service_info是否存在
    :param xpath:
    :return: True/False
    '''
    try:
        serve_list = xpath.xpath("//div[@class='doctor-recommend']/div/div[1]/text()")
        if str(serve_list[0]) == '--' and str(serve_list[1]) == '--' and str(serve_list[2]) == '--':
            return False
        else:
            return True
    except IndexError:
        return False

def is_comment_label_exist(xpath):
    '''
    判断医生pc详情页的comment_label是否存在
    :param xpath:
    :return: True/False
    '''
    label_num_list = xpath.xpath("//ul[@class='tags']/li/span/text()")
    if len(label_num_list) == 0: return False
    else: return True

def is_mobile_comment_label_exist(xpath):
    '''
    判断医生mobile详情页的comment_label是否存在
    :param xpath:
    :return: True/False
    '''
    comment_list = xpath.xpath("//div[@class='sec sec-assess-info']/div[2]/span/i/text()")
    if len(comment_list) == 0:
        return False
    else:
        return True

def is_illness_question_exist(json):
    '''
    判断医生是否存在好评问题
    :param xpath:
    :return: True/False
    '''
    if json is None: return False
    problem_list = json["problem_list"]
    if len(problem_list) == 0: return False
    else: return True

def is_reward_exist(html):
    '''
    判断医生详情页的reward是否存在
    :param html:
    :return: True/False
    '''
    try:
        if '心意墙' in html:
            return True
        else:
            return False
    except Exception as e:
        logger.warning("判断医生详情页的reward是否存在出错，详情 {}".format(e))
        return False

