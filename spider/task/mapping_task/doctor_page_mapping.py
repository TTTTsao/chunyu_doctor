import random
import time
import datetime

from spider.db.dao.doctor_dao import *
from spider.db.dao.hospital_dao import *
from spider.db.dao.clinic_dao import ClinicOper

from spider.page_get.chunyu_request import doctor_page_request as dr
from spider.page_parse.field_parse import doctor_parse as dp
from spider.page_parse.basic import *
from spider.decorators.crawl_decorator import crawl_decorator
from spider.util.basic import (check_db_exist, check_db_today, check_db_interval)
from spider.util.log_util import create_crawl_logger
logger = create_crawl_logger()
logger.remove()

@crawl_decorator
def recommend_doctor_mapping(clinic_id):
    '''
    【科室每日推荐-医生（含可咨询+不可咨询）-日更】共26页
    :param clinic_id: 科室id
    :return:
    '''
    page = 1
    while page < 27:
        html = dr.get_recommend_doctor_page(clinic_id, page)
        if html is None:
            logger.warning("科室 {} 第 {} 页为None".format(clinic_id, page))
        elif is_404(html):
            logger.warning("科室 {} 第 {} 页为404页面".format(clinic_id, page))
        elif is_page_has_no_info(html):
            logger.warning("科室 {} 第 {} 页暂无医生信息".format(clinic_id, page))
        else:
            recommend_doctors = dp.clinic_html_2_recommend_doctor(clinic_id, html)
            doctor_base_datas = dp.clinic_html_2_doctor_base(clinic_id, html)
            doctor_img_datas = dp.clinic_html_2_doctor_img(clinic_id, html)
            hospital_base_datas = dp.clinci_html_2_hospital_base(clinic_id, html)

            DoctorRecommendOper.add_doctor_recommend_with_query(recommend_doctors)
            DoctorBaseInfoOper.add_doctor_base_with_query(doctor_base_datas)
            DoctorImgOper.add_doctor_img_with_query(doctor_img_datas)
            HospitalOper.add_hospital_base_with_query(hospital_base_datas)

            time.sleep(random.uniform(1, 2))
            logger.info("科室 {} 第 {} 页抓取完毕".format(clinic_id, page))
            page += 1
    logger.info("科室 {} 抓取完毕".format(clinic_id))

@crawl_decorator
def doctor_detail_page_status_mapping(doctor_id, interval_hours):
    '''
    【医生详情页面状态信息-月更】
    :param doctor_id:医生id
    :return:
    '''
    if not check_db_interval('estimate_doctor_crawl_status', [{'k': 'doctor_id', "v": doctor_id}], interval_hours):
        html = dr.get_doctor_moblie_detail_page(doctor_id)
        if html is None:
            logger.warning("医生 {} 页面为None".format(doctor_id))
            doctor_status_data = dp.anti_crawl_doctor_status(doctor_id)
        elif is_404(html):
            logger.warning("医生 {} 页面为 404 页面".format(doctor_id))
            doctor_status_data = dp.return_404_doctor_status(doctor_id)
        elif not is_doctor_mobile_detail_page_right(doctor_id, html):
            logger.warning("医生 {} 页面被反爬，稍后重新爬取".format(doctor_id))
            doctor_status_data = dp.anti_crawl_doctor_status(doctor_id)
            doctor_info_mapping(html)
        else:
            doctor_status_data = dp.doctor_mobile_page_html_2_doctor_status(doctor_id, html)
            json = dr.get_doctor_illness_init_json(doctor_id)
            if is_illness_question_exist(json):
                doctor_status_data.is_illness_question_exist = 1
            else:
                doctor_status_data.is_illness_question_exist = 0
        if not check_db_exist('estimate_doctor_crawl_status', [{'k': 'doctor_id', "v": doctor_id}]):
            DoctorStatusOper.add_one(doctor_status_data)
        else:
            DoctorStatusOper.update_status_by_data(doctor_status_data)

@crawl_decorator
def doctor_anti_crawl_detail_page_status_mapping(doctor_id):
    '''
    被反爬后重新抓取医生mobile页面状态信息
    :param doctor_id:
    :return:
    '''
    html = dr.get_doctor_moblie_detail_page(doctor_id)
    if html is None:
        logger.warning("医生 {} 页面为None".format(doctor_id))
        doctor_status_data = dp.anti_crawl_doctor_status(doctor_id)
    elif is_404(html):
        logger.warning("医生 {} 页面为 404 页面".format(doctor_id))
        doctor_status_data = dp.return_404_doctor_status(doctor_id)
    elif not is_doctor_mobile_detail_page_right(doctor_id, html):
        logger.warning("医生 {} 页面被反爬，稍后重新爬取".format(doctor_id))
        doctor_status_data = dp.anti_crawl_doctor_status(doctor_id)
        doctor_info_mapping(html)
    else:
        doctor_status_data = dp.doctor_mobile_page_html_2_doctor_status(doctor_id, html)
        json = dr.get_doctor_illness_init_json(doctor_id)
        if is_illness_question_exist(json):
            doctor_status_data.is_illness_question_exist = 1
        else:
            doctor_status_data.is_illness_question_exist = 0
    if not check_db_exist('estimate_doctor_crawl_status', [{'k': 'doctor_id', "v": doctor_id}]):
        DoctorStatusOper.add_one(doctor_status_data)
    else:
        DoctorStatusOper.update_status_by_data(doctor_status_data)

@crawl_decorator
def doctor_info_mapping(html):
    '''
    被反爬后，解析返回的数据(mobile)
    :param html: 被反爬后返回的医生详情页
    :return:
    '''
    doctor_id, doctor_base, doctor_price, doctor_comment, doctor_reward = dp.doctor_mobile_page_html_2_doctor_detail(html)
    doctor_status_data = dp.doctor_mobile_page_html_2_doctor_status(doctor_id, html)
    json = dr.get_doctor_illness_init_json(doctor_id)
    if is_illness_question_exist(json):
        doctor_status_data.is_illness_question_exist = 1
    else:
        doctor_status_data.is_illness_question_exist = 0
    if not check_db_exist('estimate_doctor_crawl_status', [{'k': 'doctor_id', "v": doctor_id}]) and doctor_status_data is not None:
        DoctorStatusOper.add_one(doctor_status_data)
    else:
        DoctorStatusOper.update_status_by_data(doctor_status_data)
    if not check_db_exist('raw_doctor_base_info', [{'k': 'doctor_id', "v": doctor_id}]) and doctor_base is not None:
        DoctorBaseInfoOper.add_one(doctor_base)
    if not check_db_today('raw_doctor_price', [{'k': 'doctor_id', "v": doctor_id}]):
        if doctor_price.doctor_price_type == '暂无问诊服务' or doctor_price is None:
            pass
        else:
            DoctorPriceOper.add_one(doctor_price)
    if not check_db_today('raw_doctor_comment_label', [{'k': 'doctor_id', "v": doctor_id}]) and doctor_comment is not None:
        DoctorCommentLabelOper.add_one(doctor_comment)
    if not check_db_interval('raw_doctor_reward', [{'k': 'doctor_id', "v": doctor_id}], 24 * 30) and doctor_reward is not None:
        DoctorRewardOper.add_all(doctor_reward)


@crawl_decorator
def doctor_high_frequency_info_mapping(doctor_id):
    '''
    【医生高频更新信息-日更】
    医生价格
    医生服务信息(会被反爬，不做增加，只做更新)
    医生评价标签数量
    :param doctor_id: 医生id
    :return:
    '''
    html = dr.get_doctor_moblie_detail_page(doctor_id)
    if html is None:
        logger.warning("医生 {} 页面为None".format(doctor_id))
        doctor_high_frequency_data = dp.anti_crawl_doctor_high_frequency_status(doctor_id)
        DoctorHighFrequencyStatusOper.update_staus_with_data(doctor_high_frequency_data)
    elif is_404(html):
        logger.warning("医生 {} 页面为 404 页面".format(doctor_id))
        doctor_status_data = dp.return_404_doctor_status(doctor_id)
        DoctorStatusOper.update_status_by_data(doctor_status_data)
    elif not is_doctor_mobile_detail_page_right(doctor_id, html):
        logger.warning("医生 {} 页面被反爬，稍后重新爬取".format(doctor_id))
        doctor_high_frequency_data = dp.anti_crawl_doctor_high_frequency_status(doctor_id)
        DoctorHighFrequencyStatusOper.update_staus_with_data(doctor_high_frequency_data)
        doctor_info_mapping(html)
    else:
        price_data = dp.doctor_mobile_page_html_2_doctor_price(doctor_id, html)
        serve_data = dp.doctor_mobile_page_html_2_doctor_service_info(doctor_id, html)
        comment_data = dp.doctor_mobile_page_html_2_doctor_comment_label(doctor_id, html)
        if not check_db_today('raw_doctor_price', [{'k': 'doctor_id', "v": doctor_id}]):
            if price_data.doctor_price_type == '暂无问诊服务' or price_data is None:
                DoctorStatusOper.update_status_by_price(DoctorStatus(doctor_id=doctor_id, is_page_404=1, is_anti_crawl=1, is_price_exist=0))
            else:
                DoctorPriceOper.add_one(price_data)
        if not check_db_today('raw_doctor_service_info', [{'k': 'doctor_id', "v": doctor_id}]) and serve_data is not None:
            DoctorServiceInfoOper.add_one(serve_data)
        if not check_db_today('raw_doctor_comment_label', [{'k': 'doctor_id', "v": doctor_id}]) and comment_data is not None:
            DoctorCommentLabelOper.add_one(comment_data)
        DoctorHighFrequencyStatusOper.update_staus_with_data(DoctorHighFrequencyStatus(
            doctor_id=doctor_id,
            is_price_crawl=1,
            is_service_info_crawl=1,
            is_comment_label_crawl=1
        ))

@crawl_decorator
def doctor_mid_frequency_info_mapping(doctor_id, interval_hours):
    '''
    【医生中频更新信息-月更】
    医生心意墙信息
    :param doctor_id:
    :param interval_hours: 720h
    :return:
    '''
    if check_db_interval('raw_doctor_reward', [{'k': 'doctor_id', "v": doctor_id}], interval_hours):
        pass
    else:
        html = dr.get_doctor_detail_page(doctor_id)
        if html is None:
            logger.warning("医生 {} 页面为None".format(doctor_id))
        elif is_404(html):
            logger.warning("医生 {} 页面为 404 页面".format(doctor_id))
        elif not is_doctor_detail_page_right(doctor_id, html):
            logger.warning("医生 {} 页面被反爬，稍后重新爬取".format(doctor_id))
        else:
            reward_datas = dp.doctor_page_html_2_doctor_reward(doctor_id, html)
            if reward_datas is not None: DoctorRewardOper.add_all(reward_datas)

    
@crawl_decorator
def doctor_low_frequency_info_mapping(doctor_id):
    '''
    【医生低频更新信息】：当存在于base_info中而不存在于此
    医生认证信息
    医生个人标签信息
    医生简介信息
    :param doctor_id:
    :param interval_hours:
    :return:
    '''
    html = dr.get_doctor_detail_page(doctor_id)
    if html is None:
        logger.warning("医生 {} 页面为None".format(doctor_id))
    elif is_404(html):
        logger.warning("医生 {} 页面为 404 页面".format(doctor_id))
    elif not is_doctor_detail_page_right(doctor_id, html):
        logger.warning("医生 {} 页面被反爬，稍后重新爬取".format(doctor_id))
    else:
        auth_data = dp.doctor_page_html_2_doctor_auth_info(doctor_id, html)
        if not check_db_exist("raw_doctor_auth_info", [{'k': 'doctor_id', "v": doctor_id}]) and auth_data is not None:
            DoctorAuthInfoOper.add_one(auth_data)
        elif auth_data is not None:
            DoctorAuthInfoOper.update_auth_info_by_doctor_id(auth_data)
        tag_data = dp.doctor_page_html_2_doctor_tag(doctor_id, html)
        if not check_db_exist("raw_doctor_tag", [{'k': 'doctor_id', "v": doctor_id}]) and tag_data is not None:
            DoctorTagOper.add_one(tag_data)
        elif tag_data is not None:
            DoctorTagOper.update_tag_by_doctor_id(tag_data)
        des_data = dp.doctor_page_html_2_doctor_description(doctor_id, html)
        if not check_db_exist("raw_doctor_description", [{'k': 'doctor_id', "v": doctor_id}]) and des_data is not None:
            DoctorDescriptionOper.add_one(des_data)
        elif des_data is not None:
            DoctorDescriptionOper(des_data)
        hospital, clinic, hospital_clinic = dp.doctor_page_html_2_hospital_and_clinic_base(doctor_id, html)
        if not check_db_exist("raw_hospital", [{'k': 'hospital_id', "v": hospital.hospital_id}]) and hospital is not None:HospitalOper.add_one(hospital)
        if not check_db_exist("raw_hospital_clinic_base_info", [{'k': 'hospital_clinic_id', "v": clinic.hospital_clinic_id}]) and clinic is not None:HospitalClinicBaseInfoOper.add_one(clinic)
        if not check_db_exist("raw_hospital_clinic_enter_doctor", [{'k': 'hospital_clinic_id', "v": hospital_clinic.hospital_clinic_id}]) and hospital_clinic is not None:HospitalClinicEnterDoctorOper.add_one(hospital_clinic)


@crawl_decorator
def doctor_question_mapping(doctor_id):
    '''
    医生问诊对话部分信息（ajax获取）
    :param doctor_id: 医生id
    :return:
    '''
    json = dr.get_doctor_illness_init_json(doctor_id)
    if json is None:
        logger.warning("医生 {} 好评问题为None".format(doctor_id))
    else:
        hot_json = json["hot_consults"]
        if hot_json is not None:
            hot_consults = []
            for item in hot_json:
                hot_consults.append(item["keywords"])
            for item in hot_consults:
                cur_page = 1
                flag = True
                while flag:
                    if cur_page == 1:
                        doctor_questions = dp.doctor_inquiry_json_2_doctor_question(doctor_id, json, item)
                        if doctor_questions is not None: DoctorIllnessOper.add_all(doctor_questions)
                        cur_page += 1
                        flag = json["has_more_page"]
                    else:
                        page_json = dr.get_doctor_illness_json_with_page(doctor_id, cur_page, item)
                        if cur_page == page_json["query_info"]["page"]:
                            doctor_questions = dp.doctor_inquiry_json_2_doctor_question(doctor_id, page_json, item)
                            if doctor_questions is not None:DoctorIllnessOper.add_all(doctor_questions)
                            cur_page += 1
                            flag = page_json["has_more_page"]
                        else:
                            flag = False
        elif json["problem_list"] is not None:
            cur_page = 1
            flag = True
            while flag:
                if cur_page == 1:
                    doctor_questions = dp.doctor_inquiry_json_2_doctor_question(doctor_id, json, type_item=None)
                    if doctor_questions is not None: DoctorIllnessOper.add_all(doctor_questions)
                    cur_page += 1
                    flag = json["has_more_page"]
                else:
                    page_json = dr.get_doctor_illness_json_with_page(doctor_id, cur_page, type_item=None)
                    if cur_page == page_json["query_info"]["page"]:
                        doctor_questions = dp.doctor_inquiry_json_2_doctor_question(doctor_id, page_json, type_item=None)
                        if doctor_questions is not None:DoctorIllnessOper.add_all(doctor_questions)
                        cur_page += 1
                        flag = page_json["has_more_page"]
                    else:
                        flag = False
        else:
            logger.warning("医生 {} 好评问题为None".format(doctor_id))

@crawl_decorator
def question_html_mapping(question_id):
    '''
    医生问诊对话详情信息（html获取）
    :param question_id: 医生id
    :return:
    '''
    html = dr.get_doctor_inquiry_detail_page(question_id)
    if html is None:
        logger.warning("医生问诊对话 {} 页面为None".format(question_id))
    elif is_404(html):
        logger.warning("医生问诊对话 {} 页面为 404 页面".format(question_id))
    elif not is_illness_detail_page_right(question_id, html):
        logger.warning("医生问诊对话 {} 页面被反爬，稍后重新爬取".format(question_id))
    else:
        illness_data = dp.question_html_2_doctor_quesstion_clinic_and_html(question_id, html)
        if illness_data is not None: DoctorIllnessOper.update_illness_by_question_id(illness_data)


def doctor_serve_mapping(doctor_id):
    '''
    【医生中频更新信息】：当存在于base_info中而不存在于此
    医生服务信息[只有当不被反爬时才抓取，不获取反爬页面数据]
    :param doctor_id:
    :return:
    '''
    html = dr.get_doctor_detail_page(doctor_id)
    if html is None:
        logger.warning("医生 {} 页面为None".format(doctor_id))
    elif is_404(html):
        logger.warning("医生 {} 页面为 404 页面".format(doctor_id))
    elif not is_doctor_detail_page_right(doctor_id, html):
        logger.warning("医生 {} 页面被反爬，稍后重新爬取".format(doctor_id))
    else:
        serve_data = dp.doctor_page_html_2_doctor_service_info(doctor_id, html)
        if not check_db_exist("raw_doctor_service_info", [{'k': 'doctor_id', "v": doctor_id}]) and serve_data is not None:
            DoctorServiceInfoOper.add_one(serve_data)
        elif serve_data is not None:
            DoctorServiceInfoOper.update_service_info_by_doctor_id(serve_data)