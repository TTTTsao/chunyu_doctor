import json
from lxml import etree
from bs4 import BeautifulSoup
from spider.db.models import *
from spider.db.dao.doctor_dao import *
from spider.page_get.chunyu_request.doctor_page_request import get_doctor_illness_init_json
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import *
from spider.util.basic import trans_to_datetime
from spider.util.reg.reg_doctor import *
from spider.util.reg.reg_hospital import *
from spider.util.log_util import create_parse_logger
logger = create_parse_logger()
logger.remove()

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_status(doctor_id, html):
    '''
    根据医生mobile详情页获取医生页面状态
    :param doctor_id: 医生id
    :param html: 医生mobile详情页
    :return: 医生页面状态/None
    '''
    xpath = etree.HTML(html)
    return DoctorStatus(
        doctor_id=doctor_id,
        is_page_404=1,
        is_anti_crawl=1,
        is_price_exist=1 if is_mobile_price_exist(xpath) else 0,
        is_service_info_exist=1 if is_mobile_service_info_exist(xpath) else 0,
        is_comment_label_exist=1 if is_mobile_comment_label_exist(xpath) else 0,
        is_reward_exist=1 if is_reward_exist(html) else 0
    )

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_detail(html):
    '''
    获取mobile反爬页面的医生数据信息
    :param html: 反爬数据
    :return: 医生mobile详情页面数据
    '''
    xpath = etree.HTML(html)
    try:
        doctor_id = xpath.xpath("//input[1]/@data-doctor-id")[0]
        doctor_name = xpath.xpath("//body/div[2]/@data-name")[0]
        doctor_base = DoctorBaseInfo(doctor_id=doctor_id, doctor_name=doctor_name)
        doctor_price = doctor_mobile_page_html_2_doctor_price(doctor_id, html)
        doctor_comment = doctor_mobile_page_html_2_doctor_comment_label(doctor_id, html)
        doctor_reward = doctor_mobile_page_html_2_doctor_reward(doctor_id, html)
        return doctor_id, doctor_base, doctor_price, doctor_comment, doctor_reward
    except Exception as e:
        logger.error("解析医生 {} 移动端反爬页面的医生数据信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_description(doctor_id, html):
    '''
    【废弃】解析医生mobile详情页面-简介信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生简介信息对象/None(错误)
    '''
    xpath = etree.HTML(html)
    try:
        major = xpath.xpath("//div[@id='doctor-home-preview']/div[2]/div[2]/text()")
        edu = xpath.xpath("//div[@id='doctor-home-preview']/div[3]/div[2]/text()")
        return DoctorDescription(
            doctor_id=doctor_id,
            doctor_description_major=major[0] if len(major) != 0 else None,
            doctor_description_edu_background=edu[0] if len(edu) != 0 else None
        )
    except Exception as e:
        logger.error("解析医生 {} 移动端页面医生简介信息失败，错误详情 {}".format(doctor_id, e))
        return None


@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_service_info(doctor_id, html):
    '''
    【废弃】解析医生mobile详情页面-服务信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生服务信息对象/None(错误)
    '''
    xpath = etree.HTML(html)
    try:
        serve_list = xpath.xpath("//div[@class='rec-lable']/text()")
        followers = int(xpath.xpath("//*[@id='sec-subscribe-wechat-id']/div[3]/div/span[@class='qr-code-num']/text()")[0])
        return DoctorServiceInfo(
            doctor_id=doctor_id,
            doctor_serve_nums=int(serve_list[0]) if str(serve_list[0]) != '--' else 0,
            doctor_serve_favorable_rate=Decimal(serve_list[1]) if str(serve_list[1]) != '--' else 0,
            doctor_serve_peer_recognization=int(serve_list[2]) if str(serve_list[2]) != '--' else 0,
            doctor_serve_followers=followers
        )
    except Exception as e:
        logger.error("解析医生 {} 移动端页面服务信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_comment_label(doctor_id, html):
    '''
    解析医生mobile详情页面-评价信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生评价信息对象/None(错误)
    '''
    xpath = etree.HTML(html)
    try:
        comment_list = xpath.xpath("//div[@class='sec sec-assess-info']/div[2]/span/i/text()")
        return DoctorCommentLabel(
            doctor_id=doctor_id,
            doctor_comment_attitude=get_reg_label_num(str(comment_list[0])) if len(comment_list) != 0 else 0,
            doctor_comment_explanation=get_reg_label_num(str(comment_list[1])) if len(comment_list) != 0 else 0,
            doctor_comment_reply=get_reg_label_num(str(comment_list[2])) if len(comment_list) != 0 else 0,
            doctor_comment_suggestion=get_reg_label_num(str(comment_list[3])) if len(comment_list) != 0 else 0
        )
    except Exception as e:
        logger.error("解析医生 {} 移动端页面评价信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_price(doctor_id, html):
    '''
    解析医生mobile详情页面-价格信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生价格对象/None(错误)
    '''
    xpath = etree.HTML(html)
    try:
        raw_price = xpath.xpath("//div[@id='referring-physician']/div[2]/div[@class='rp-head']/div/div[1]/text()")[0]
        discount = Decimal(xpath.xpath("//body/div[2]/@data-discount-price")[0])
        price = Decimal(get_reg_mobile_price(str(raw_price)))
        return DoctorPrice(
            doctor_id=doctor_id,
            doctor_price=price if price != -1 else None,
            doctor_price_discount=discount if discount != 0 else None,
            doctor_price_type='图文咨询' if price != -1 else '暂无问诊服务'
        )
    except Exception as e:
        logger.error("解析医生 {} 移动端页面价格信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_reward(doctor_id, html):
    '''
    解析医生mobile详情页面-心意墙信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生心意墙对象/None(错误)
    '''
    if is_reward_exist(html):
        xpath = etree.HTML(html)
        try:
            rewards_data = []
            date_list = xpath.xpath("//div[@class='sec sec-assess-info']/div[@class='assess-item']/div[1]/span/text()")
            num_list = xpath.xpath("//div[@class='sec sec-assess-info']/div[@class='assess-item']/div[1]/h6/span/i/text()")
            content_list = xpath.xpath("//div[@class='sec sec-assess-info']/div[@class='assess-item']/div[2]/text()")

            for i in range(len(date_list)):
                rewards_data.append(DoctorReward(
                    doctor_id=doctor_id,
                    doctor_reward_datetime=trans_to_datetime(str(date_list[i])),
                    doctor_reward_amount=int(num_list[i]),
                    doctor_reward_content=str(content_list[i])
                ))
            return rewards_data
        except Exception as e:
            logger.error("解析医生 {} 移动端页面心意墙信息失败，错误详情 {}".format(doctor_id, e))
            return None
    else:
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_auth_info(doctor_id, html):
    '''
    解析pc页医生认证信息-auth
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: auth认证信息对象/None（错误）
    '''
    xpath = etree.HTML(html)
    try:
        hospital_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[2]/a/@href")[0]
        clinic_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/a[1]/@href")[0]
        auth_grade = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[2]/text()")[0]
        auth_time = xpath.xpath("//div[@class='tip-inner']//div[@class='content-wrap']/div[3]/div[2]/text()")[0]
        auth_status = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[3]/text()")[0]

        return DoctorAuthInfo(
            doctor_id=doctor_id,
            doctor_auth_hospital_id=get_reg_hospital_id(str(hospital_id)),
            doctor_auth_clinic_id=get_reg_clinic_id(str(clinic_id)),
            doctor_auth_grade=str(auth_grade),
            doctor_auth_time=get_reg_auth_time(str(auth_time)),
            doctor_auth_status=1 if str(auth_status) == "已认证" else 0
        )
    except Exception as e:
        logger.error("解析 {} 医生auth认证信息错误，详情：{}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_tag(doctor_id, html):
    '''
    解析医生个人标签信息-tag
    :param doctor_id:
    :param html:
    :return: 个人标签tag信息对象/None（错误）
    '''
    doctor_tag = DoctorTag()
    xpath = etree.HTML(html)
    doctor_tag.doctor_id = doctor_id
    try:
        tag_content_dict = {}
        label_list = xpath.xpath("//div[@class='doctor-hospital']/span/text()")
        # 判断有几个标签
        for i in range(len(label_list)):
            label_name = 'label' + str(i + 1)
            tag_content_dict[label_name] = label_list[i]

        tag_content_json = json.dumps(tag_content_dict, ensure_ascii=False)
        doctor_tag.tag_content = tag_content_json
        return doctor_tag
    except Exception as e:
        logger.error("解析 {} 医生tag信息错误，详情：{}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_service_info(doctor_id, html):
    '''
    解析医生pc详情页面-服务信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生服务信息对象/None(错误)
    '''
    xpath = etree.HTML(html)

    try:
        serve_nums = xpath.xpath("//ul[@class='doctor-data']/li[1]/span[1]/text()")[0]
        favorable_rate = xpath.xpath("//ul[@class='doctor-data']/li[2]/span[1]/text()")[0]
        peer_recognization = xpath.xpath("//ul[@class='doctor-data']/li[3]/span[1]/text()")[0]
        patient_praise_num = xpath.xpath("//ul[@class='doctor-data']/li[4]/span[1]/text()")[0]
        followers = xpath.xpath("//div[@class='wexin-qr-code']//div[@class='footer-des']/text()")[0]

        return DoctorServiceInfo(
            doctor_id=doctor_id,
            doctor_serve_nums=0 if str(serve_nums) == '--' else int(serve_nums),
            doctor_serve_favorable_rate=0 if str(favorable_rate) == '--' else int(favorable_rate),
            doctor_serve_peer_recognization=0 if str(peer_recognization) == '--' else Decimal(peer_recognization),
            doctor_serve_patient_praise_num=0 if str(patient_praise_num) == '--' else int(patient_praise_num),
            doctor_serve_followers=get_reg_followers(str(followers))
        )
    except Exception as e:
        logger.error("解析医生 {} 页面服务信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_price(doctor_id, html):
    '''
    解析pc医生详情页面-价格信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生价格对象/None(错误)
    '''
    doctor_price_data = DoctorPrice()
    doctor_price_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    try:
        price = xpath.xpath("//a[@class='doctor-pay-wrap']/div[@class='doctor-pay-consult']/span/text()")
        price_type = xpath.xpath("//a[@class='doctor-pay-wrap']/div[@class='doctor-pay-consult']/text()")
        discount = xpath.xpath("//a[@class='doctor-pay-wrap']/span[@class='discont-text']/text()")

        return DoctorPrice(
            doctor_id=doctor_id,
            doctor_price_type=get_reg_price_type(str(price_type[0])) if len(price) > 0 else '暂无问诊服务',
            doctor_price=Decimal(price[0]) if len(price) > 0 else None,
            doctor_price_discount=get_reg_price_discount(str(discount[0])) if len(discount) != 0 else None
        )
    except Exception as e:
        logger.error("解析医生 {} 页面价格信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_description(doctor_id, html):
    '''
    解析pc医生详情页面-简介信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生简介对象/None(错误)
    '''
    doctor_description_data = DoctorDescription()
    doctor_description_data.doctor_id = doctor_id

    xpath = etree.HTML(html)
    try:
        # 增加页面元素判断，是否存在某某字段-先判断是否有4个，有3个（无专业擅长）再做详细判断
        temp_length = len(xpath.xpath("//p[@class='detail']"))
        return DoctorDescription(
            doctor_id=doctor_id,
            doctor_description_edu_background=get_reg_doctor_profile(str(xpath.xpath("//p[@class='detail']/text()")[1])),
            doctor_description_major=get_reg_doctor_profile(str(xpath.xpath("//p[@class='detail']/text()")[3])) if temp_length == 4 else None,
            doctor_description_description=get_reg_doctor_profile(str(xpath.xpath("//p[@class='detail']/text()")[5])) if temp_length == 4 else get_reg_doctor_profile(str(xpath.xpath("//p[@class='detail']/text()")[3])),
            doctor_description_hospital_location=get_reg_doctor_profile(str(xpath.xpath("//p[@class='detail']/text()")[7])) if temp_length == 4 else get_reg_doctor_profile(str(xpath.xpath("//p[@class='detail']/text()")[5]))
        )
    except Exception as e:
        logger.error("解析 {} 医生个人简介信息错误，详情：{}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_comment_label(doctor_id, html):
    '''
    解析医生详情页面-评价标签数量信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生评价标签数量对象/None(错误)
    '''
    xpath = etree.HTML(html)
    try:
        label_num_list = xpath.xpath("//ul[@class='tags']/li/span/text()")
        return DoctorCommentLabel(
            doctor_id=doctor_id,
            doctor_comment_attitude=0 if len(label_num_list) == 0 else get_reg_label_num(str(label_num_list[0])),
            doctor_comment_explanation=0 if len(label_num_list) == 0 else get_reg_label_num(str(label_num_list[1])),
            doctor_comment_reply=0 if len(label_num_list) == 0 else get_reg_label_num(str(label_num_list[2])),
            doctor_comment_suggestion=0 if len(label_num_list) == 0 else get_reg_label_num(str(label_num_list[3]))
        )
    except Exception as e:
        logger.error("解析医生 {} 页面评价标签数量信息失败，错误详情 {}".format(doctor_id, e))
        return None

@parse_decorator(False)
def doctor_page_html_2_doctor_reward(doctor_id, html):
    '''
    解析医生详情页面-医生心意墙信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生心意墙对象/None(错误)
    '''
    xpath = etree.HTML(html)
    doctor_reward_datas = []
    try:
        reward_datetime_list = xpath.xpath("//ul[@class='money-list ']/li/span/text()")
        reward_amount_list = xpath.xpath("//ul[@class='money-list ']/li/div/span[1]/i/text()")
        reward_content_list = xpath.xpath("//ul[@class='money-list ']/li/div/span[2]/text()")
        if len(reward_content_list) == 0:
            return None
        else:
            for i in range(len(reward_content_list)):
                doctor_reward_datas.append(DoctorReward(
                    doctor_id=doctor_id,
                    doctor_reward_datetime=trans_to_datetime(str(reward_datetime_list[i])),
                    doctor_reward_amount=get_reg_reward_amount(str(reward_amount_list[i])),
                    doctor_reward_content=str(reward_content_list[i])
                ))
            return doctor_reward_datas
    except Exception as e:
        logger.error("解析医生 {} 页面心意墙信息失败，错误详情 {}".format(doctor_id, e))
        return None

def doctor_page_html_2_hospital_and_clinic_base(doctor_id, html):
    '''
    解析医生详情页面-医院信息、科室信息（仅未爬过）
    [医院信息]:hospital_id、hospital_name
    [科室信息]:hospital_id、clinic_id、clinic_name
    :param html:
    :return:
    '''
    xpath = etree.HTML(html)
    try:
        hospital_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[2]/a/@href")[0]
        hospital_name = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[2]/a/text()")[0]
        clinic_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/a[1]/@href")[0]
        clinic_name = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/a[1]/text()")[0]

        hospital = Hospital(hospital_id=get_reg_hospital_id(str(hospital_id)), hospital_name=get_reg_clinic_name(str(hospital_name)))
        clinic = HospitalClinicBaseInfo(hospital_clinic_id=get_reg_clinic_id(str(clinic_id)), hospital_clinic_name=get_reg_clinic_name(str(clinic_name)))
        hospital_clinic = HospitalClinicEnterDoctor(hospital_id=get_reg_hospital_id(str(hospital_id)), hospital_clinic_id=get_reg_clinic_id(str(clinic_id)))
        return hospital, clinic, hospital_clinic
    except Exception as e:
        logger.error("解析医生 {} 页面医院和科室信息失败，错误详情 {}".format(doctor_id, e))
        return None, None, None



@parse_decorator(False)
def doctor_inquiry_json_2_doctor_question(doctor_id, json, type_item):
    '''
    解析医生好评问题json
    :param doctor_id: 医生id
    :param json: 医生好评问题json
    :param type_item: 问题类型（str/None【不存在类型】）
    :return: 医生好评问题不完整对象/None（错误）
    '''
    problem_list = json["problem_list"]
    question_datas = []
    try:
        for problem in problem_list:
            question_datas.append(IllnessInfo(
                doctor_id=doctor_id,
                illness_question_id=problem["id"],
                illness_title=problem["title"],
                illness_time=trans_to_datetime(problem["date_str"]),
                illness_type=type_item if type_item is not None else None,
                illness_ask=problem["ask"],
                illness_answer=problem["answer"]
            ))
        return question_datas
    except Exception as e:
        logger.error("解析医生 {} AJAX页面问题信息失败，错误详情 {}".format(doctor_id, e))
        return None


@parse_decorator(False)
def question_html_2_doctor_quesstion_clinic_and_html(question_id, html):
    '''
    解析医生好评问题对话html页面
    :param question_id: 问题id
    :param html: 好评问题详情页面
    :return: 医生问诊对话对象/None（错误）
    '''
    soup = BeautifulSoup(html, 'lxml')
    try:
        clinic_name = soup.find(name='div', class_="bread-crumb-spacial").find(name='a').get_text()
        dialog_list = soup.find_all(name='div', class_='context-left')
        dialog_str = ''
        for item in dialog_list:
            people = item.find(name='h6', class_='doctor-name').get_text()
            dialog = item.find(name='p').get_text().strip().replace("\n", '')
            dialog_str = dialog_str + people + ":" + dialog + "\n"

        return Dialog(
            inquiry_question_id=question_id,
            clinic_name=clinic_name,
            inquiry_dialog=dialog_str
        )
    except Exception as e:
        logger.info("解析医生 {} 问诊对话页面信息失败，错误详情 {}".format(question_id, e))
        return None


@parse_decorator(False)
def doctor_topic_json_2_doctor_topic(doctor_id, json):
    if json is None:
        return
    pass

@parse_decorator(False)
def clinic_html_2_recommend_doctor(clinic_id, html):
    '''
    【根据科室找医生】页面->每日推荐医生（包含可咨询和不可咨询）
    :param clinic_id: 科室id
    :param html: response.text
    :return: 推荐医生对象/None（出错）
    '''
    xpath = etree.HTML(html)
    recommend_doctor_datas = []
    try:
        doctor_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[1]/a/@href")
        hospital_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[2]/a/@href")

        for i in range(len(doctor_id_list)):
            raw_available_status = xpath.xpath(
                f"//div[@class='doctor-list']/div[{i + 1}]/div[@class='avatar-wrap']/span/text()")

            recommend_doctor_datas.append(DoctorRecommend(
                doctor_id=get_reg_doctor_id(str(doctor_id_list[i])),
                hospital_id=get_reg_hospital_id(str(hospital_id_list[i])),
                clinic_id=clinic_id,
                recommend_doctor_is_inquiry=1 if len(raw_available_status) > 0 else 0
            ))
        return recommend_doctor_datas
    except Exception as e :
        logger.warning("科室 {} 页面解析错误, 详情 {}".format(clinic_id, e))
        return None


@parse_decorator(False)
def clinic_html_2_recommend_available_doctor(clinic_id, html):
    '''
    【根据科室找医生】页面->每日推荐医生（仅可咨询）
    :param clinic_id: 科室id
    :param html: response.text
    :return: 推荐医生对象/None（出错）
    '''
    if html is None:
        logger.warning("科室 {} 页面为None".format(clinic_id))
        return None
    if is_404(html):
        logger.warning("科室 {} 页面为404页面".format(clinic_id))
        return None
    if is_page_has_no_info(html):
        logger.warning("科室 {} 页面暂无医生信息".format(clinic_id))
        return None

    xpath = etree.HTML(html)
    recommend_doctor_datas = []

    try:
        doctor_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[1]/a/@href")
        hospital_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[2]/a/@href")

        for i in range(len(doctor_id_list)):
            recommend_doctor_datas.append(DoctorRecommend(
                doctor_id=get_reg_doctor_id(str(doctor_id_list[i])),
                hospital_id=get_reg_hospital_id(str(hospital_id_list[i])),
                clinic_id=clinic_id,
                recommend_doctor_is_inquiry=1
            ))
        return recommend_doctor_datas
    except Exception as e:
        logger.warning("科室 {} 页面解析错误, 详情：{}".format(clinic_id,e))
        return None

@parse_decorator(False)
def clinic_html_2_doctor_base(clinic_id, html):
    '''
    【根据科室找医生】页面->医生基础信息（仅未爬过）
    :param clinic_id: 科室id
    :param html: response.text
    :return: 医生基础信息对象/None（错误）
    '''
    xpath = etree.HTML(html)
    doctor_base_datas = []

    try:
        doctor_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[1]/a/@href")
        doctor_name_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[1]/a/span[1]/text()")

        for i in range(len(doctor_id_list)):
            doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
            doctor_name = get_reg_doctor_name(str(doctor_name_list[i]))
            doctor_base_datas.append(DoctorBaseInfo(
                doctor_id=doctor_id,
                doctor_name=doctor_name
            ))
        return doctor_base_datas
    except Exception as e:
        logger.warning("科室 {} 页面解析doctor_base错误, 详情: {}".format(clinic_id, e))
        return None

def clinic_html_2_doctor_img(clinic_id, html):
    '''
    【根据科室找医生】页面->医生头像信息（仅未爬过）
    :param clinic_id: 科室id
    :param html: response.text
    :return: 医生头像信息对象/None（错误）
    '''
    xpath = etree.HTML(html)
    doctor_img_datas = []
    try:
        doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
        doctor_img_url_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[1]/a/img/@src")
        for i in range(len(doctor_id_list)):
            doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
            doctor_img = str(doctor_img_url_list[i])
            doctor_img_datas.append(DoctorImg(
                doctor_id=doctor_id,
                doctor_img_remote_path=doctor_img
            ))
        return doctor_img_datas
    except Exception as e:
        logger.warning("科室 {} 页面解析doctor_img错误, 详情: {}".format(clinic_id, e))
        return None

@parse_decorator(False)
def clinci_html_2_hospital_base(clinic_id, html):
    '''
    【根据科室找医生】页面->医院基础信息（仅未爬过）
    :param clinic_id: 科室id
    :param html: response.text
    :return:
    '''
    xpath = etree.HTML(html)
    hospital_base_datas = []

    try:
        hospital_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[2]/a/@href")
        hospital_name_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[2]/a/text()")

        for i in range(len(hospital_id_list)):
            hospital_base_datas.append(Hospital(
                hospital_id=get_reg_hospital_id(str(hospital_id_list[i])),
                hospital_name=get_reg_clinic_name(str(hospital_name_list[i]))
            ))
        return hospital_base_datas
    except Exception as e:
        logger.warning("科室 {} 页面解析hospital_base错误,详情: {}".format(clinic_id, e))
        return None

def anti_crawl_doctor_status(doctor_id):
    return DoctorStatus(
            doctor_id=doctor_id,
            is_page_404=1,
            is_anti_crawl=0
        )

def return_404_doctor_status(doctor_id):
    return DoctorStatus(
            doctor_id=doctor_id,
            is_page_404=0,
            is_anti_crawl=1,
            is_price_exist=0,
            is_comment_label_exist=0,
            is_service_info_exist=0,
            is_illness_question_exist=0,
            is_reward_exist=0,
        )

def anti_crawl_doctor_high_frequency_status(doctor_id):
    return DoctorHighFrequencyStatus(
                doctor_id=doctor_id,
                is_price_crawl=0,
                is_service_info_crawl=0,
                is_comment_label_crawl=0
            )


