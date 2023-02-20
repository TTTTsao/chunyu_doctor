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
    doctor_status_data = DoctorStatus(
        doctor_id=doctor_id,
        is_page_404=1,
        is_anti_crawl=1
    )
    # 判断各板块状态详情: price、comment、serve、reward
    if is_mobile_price_exist(xpath):
        doctor_status_data.is_price_exist = 1
    else:
        doctor_status_data.is_price_exist = 0

    if is_mobile_service_info_exist(xpath):
        doctor_status_data.is_service_info_exist = 1
    else:
        doctor_status_data.is_service_info_exist = 0

    if is_mobile_comment_label_exist(xpath):
        doctor_status_data.is_comment_label_exist = 1
    else:
        doctor_status_data.is_comment_label_exist = 0

    if is_reward_exist(html):
        doctor_status_data.is_reward_exist = 1
    else:
        doctor_status_data.is_reward_exist = 0
    return doctor_status_data

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_detail(html):
    '''
    获取mobile反爬页面的医生数据信息
    :param html: 反爬数据
    :return: 医生mobile详情页面数据
    '''
    xpath = etree.HTML(html)
    doctor_id = xpath.xpath("//input[1]/@data-doctor-id")[0]
    doctor_name = xpath.xpath("//body/div[2]/@data-name")[0]
    doctor_base = DoctorBaseInfo(
        doctor_id=doctor_id,
        doctor_name=doctor_name
    )
    doctor_price = doctor_mobile_page_html_2_doctor_price(doctor_id, html)
    doctor_comment = doctor_mobile_page_html_2_doctor_comment_label(doctor_id, html)
    doctor_reward = doctor_mobile_page_html_2_doctor_reward(doctor_id, html)
    return doctor_id, doctor_base, doctor_price, doctor_comment, doctor_reward

@parse_decorator(False)
def doctor_mobile_page_html_2_doctor_description(doctor_id, html):
    '''
    【废弃】解析医生mobile详情页面-简介信息
    :param doctor_id: 医生id
    :param html: 医生详情页面
    :return: 医生简介信息对象/None(错误)
    '''
    xpath = etree.HTML(html)
    des_data = DoctorDescription()
    des_data.doctor_id = doctor_id
    try:
        major = xpath.xpath("//div[@id='doctor-home-preview']/div[2]/div[2]/text()")
        edu = xpath.xpath("//div[@id='doctor-home-preview']/div[3]/div[2]/text()")
        if len(major) != 0:
            des_data.doctor_description_major = major[0]
        if len(edu) != 0:
            des_data.doctor_description_edu_background = edu[0]
        return des_data
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
    serve_data = DoctorServiceInfo()
    serve_data.doctor_id = doctor_id
    try:
        serve_list = xpath.xpath("//div[@class='rec-lable']/text()")
        followers = int(xpath.xpath("//*[@id='sec-subscribe-wechat-id']/div[3]/div/span[@class='qr-code-num']/text()")[0])
        serve_data.doctor_serve_followers = followers
        if len(serve_list) == 3:
            if str(serve_list[0]) == '--':
                serve_data.doctor_serve_nums = 0
            else:
                serve_data.doctor_serve_nums = int(serve_list[0])

            if str(serve_list[1]) == '--':
                serve_data.doctor_serve_favorable_rate = 0
            else:
                serve_data.doctor_serve_favorable_rate = Decimal(serve_list[1])

            if str(serve_list[2]) == '--':
                serve_data.doctor_serve_peer_recognization = 0
            else:
                serve_data.doctor_serve_peer_recognization = int(serve_list[2])
        return serve_data
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
        if len(comment_list) == 0:
            return DoctorCommentLabel(
                doctor_id=doctor_id,
                doctor_comment_attitude=0,
                doctor_comment_explanation=0,
                doctor_comment_reply=0,
                doctor_comment_suggestion=0
            )
        else:
            return DoctorCommentLabel(
                doctor_id=doctor_id,
                doctor_comment_attitude=get_reg_label_num(str(comment_list[0])),
                doctor_comment_explanation=get_reg_label_num(str(comment_list[1])),
                doctor_comment_reply=get_reg_label_num(str(comment_list[2])),
                doctor_comment_suggestion=get_reg_label_num(str(comment_list[3]))
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
    doctor_price_data = DoctorPrice()
    doctor_price_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    try:
        raw_price = xpath.xpath("//div[@id='referring-physician']/div[2]/div[@class='rp-head']/div/div[1]/text()")[0]
        discount = Decimal(xpath.xpath("//body/div[2]/@data-discount-price")[0])
        price = Decimal(get_reg_mobile_price(str(raw_price)))

        # 判断有无价格信息
        if price == -1:
            doctor_price_data.doctor_price_type = '暂无问诊服务'
        else:
            # 判断有无折扣信息
            if discount == 0:
                doctor_price_data.doctor_price_type = '图文咨询'
                doctor_price_data.doctor_price = price
            else:
                doctor_price_data.doctor_price_type = '图文咨询'
                doctor_price_data.doctor_price = price
                doctor_price_data.doctor_price_discount = discount
        return doctor_price_data
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
    doctor_auth_info = DoctorAuthInfo()
    doctor_auth_info.doctor_id = doctor_id
    try:
        hospital_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[2]/a/@href")[0]
        clinic_id = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/a[1]/@href")[0]
        auth_grade = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[2]/text()")[0]
        auth_time = xpath.xpath("//div[@class='tip-inner']//div[@class='content-wrap']/div[3]/div[2]/text()")[0]
        auth_status = xpath.xpath("//div[@class='doctor-info-item']//div[@class='detail']/div[1]/span[3]/text()")[0]

        doctor_auth_info.doctor_auth_hospital_id = get_reg_hospital_id(str(hospital_id))
        doctor_auth_info.doctor_auth_clinic_id = get_reg_clinic_id(str(clinic_id))
        doctor_auth_info.doctor_auth_grade = str(auth_grade)
        doctor_auth_info.doctor_auth_time = get_reg_auth_time(str(auth_time))

        if str(auth_status) == "已认证":
            doctor_auth_info.doctor_auth_status = 1
        else:
            doctor_auth_info.doctor_auth_status = 0
        return doctor_auth_info
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
    doctor_service_data = DoctorServiceInfo()
    doctor_service_data.doctor_id = doctor_id
    xpath = etree.HTML(html)

    try:
        serve_nums = xpath.xpath("//ul[@class='doctor-data']/li[1]/span[1]/text()")[0]
        favorable_rate = xpath.xpath("//ul[@class='doctor-data']/li[2]/span[1]/text()")[0]
        peer_recognization = xpath.xpath("//ul[@class='doctor-data']/li[3]/span[1]/text()")[0]
        patient_praise_num = xpath.xpath("//ul[@class='doctor-data']/li[4]/span[1]/text()")[0]
        followers = xpath.xpath("//div[@class='wexin-qr-code']//div[@class='footer-des']/text()")[0]

        doctor_service_data.doctor_serve_followers = get_reg_followers(str(followers))

        # 判断各值是否为'--'
        if str(serve_nums) == '--':
            doctor_service_data.doctor_serve_nums = 0
        else:
            doctor_service_data.doctor_serve_nums = int(serve_nums)

        if str(favorable_rate) == '--':
            doctor_service_data.doctor_serve_favorable_rate = 0
        else:
            doctor_service_data.doctor_serve_favorable_rate = Decimal(favorable_rate)

        if str(peer_recognization) == '--':
            doctor_service_data.doctor_serve_peer_recognization = 0
        else:
            doctor_service_data.doctor_serve_peer_recognization = Decimal(peer_recognization)

        if str(patient_praise_num) == '--':
            doctor_service_data.doctor_serve_patient_praise_num = 0
        else:
            doctor_service_data.doctor_serve_patient_praise_num = int(patient_praise_num)
        return doctor_service_data
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

        # 判断有无价格信息
        if len(price) == 0:
            doctor_price_data.doctor_price_type = '暂无问诊服务'
        else:
            # 判断有无折扣信息
            if len(discount) == 0:
                doctor_price_data.doctor_price_type = get_reg_price_type(str(price_type[0]))
                doctor_price_data.doctor_price = Decimal(price[0])
            else:
                doctor_price_data.doctor_price_type = get_reg_price_type(str(price_type[0]))
                doctor_price_data.doctor_price = Decimal(price[0])
                doctor_price_data.doctor_price_discount = get_reg_price_discount(str(discount[0]))
        return doctor_price_data
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
        if temp_length == 4:
            edu_backgroud = xpath.xpath("//p[@class='detail']/text()")[1]
            doctor_description_data.doctor_description_edu_background = get_reg_doctor_profile(str(edu_backgroud))

            major = xpath.xpath("//p[@class='detail']/text()")[3]
            doctor_description_data.doctor_description_major = get_reg_doctor_profile(str(major))

            description = xpath.xpath("//p[@class='detail']/text()")[5]
            doctor_description_data.doctor_description_description = get_reg_doctor_profile(str(description))

            hospital_location = xpath.xpath("//p[@class='detail']/text()")[7]
            doctor_description_data.doctor_description_hospital_location = get_reg_doctor_profile(
                str(hospital_location))
        elif temp_length == 3:
            edu_backgroud = xpath.xpath("///p[@class='detail']/text()")[1]
            doctor_description_data.doctor_description_edu_background = get_reg_doctor_profile(str(edu_backgroud))

            description = xpath.xpath("//p[@class='detail']/text()")[3]
            doctor_description_data.doctor_description_description = get_reg_doctor_profile(str(description))

            hospital_location = xpath.xpath("//p[@class='detail']/text()")[5]
            doctor_description_data.doctor_description_hospital_location = get_reg_doctor_profile(
                str(hospital_location))
        return doctor_description_data
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
    doctor_comment_label_data = DoctorCommentLabel()
    doctor_comment_label_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    label_num_list = xpath.xpath("//ul[@class='tags']/li/span/text()")

    try:
        # 判断是否存在【患者评价】板块
        if len(label_num_list) == 0:
            doctor_comment_label_data.doctor_comment_attitude = 0
            doctor_comment_label_data.doctor_comment_explanation = 0
            doctor_comment_label_data.doctor_comment_reply = 0
            doctor_comment_label_data.doctor_comment_suggestion = 0
        else:
            doctor_comment_label_data.doctor_comment_attitude = get_reg_label_num(str(label_num_list[0]))
            doctor_comment_label_data.doctor_comment_explanation = get_reg_label_num(str(label_num_list[1]))
            doctor_comment_label_data.doctor_comment_reply = get_reg_label_num(str(label_num_list[2]))
            doctor_comment_label_data.doctor_comment_suggestion = get_reg_label_num(str(label_num_list[3]))
        return doctor_comment_label_data
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
                doctor_reward_data = DoctorReward()

                doctor_reward_data.doctor_id = doctor_id
                doctor_reward_data.doctor_reward_datetime = trans_to_datetime(str(reward_datetime_list[i]))
                doctor_reward_data.doctor_reward_amount = get_reg_reward_amount(str(reward_amount_list[i]))
                doctor_reward_data.doctor_reward_content = str(reward_content_list[i])

                doctor_reward_datas.append(doctor_reward_data)
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
        return None



@parse_decorator(False)
def doctor_inquiry_json_2_doctor_question(doctor_id, json, type_item):
    '''
    解析医生好评问题json
    :param doctor_id: 医生id
    :param json: 医生好评问题json
    :param type_item: 问题类型（str/None【不存在类型】）
    :return: 医生好评问题不完整对象/None（错误）
    '''
    if json is None:
        return None
    problem_list = json["problem_list"]
    question_datas = []
    try:
        for problem in problem_list:
            data = IllnessInfo(
                doctor_id=doctor_id,
                illness_question_id=problem["id"],
                illness_title=problem["title"],
                illness_time=trans_to_datetime(problem["date_str"]),
                # 只抓取以上信息，clinic_id 和 对话html 后续单独抓取
            )
            if type_item is None:
                data.illness_type=''
            else:
                data.illness_type=type_item
            question_datas.append(data)
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
    xpath = etree.HTML(html)
    soup = BeautifulSoup(html, 'lxml')
    try:
        clinic_id = xpath.xpath("//div[@class='bread-crumb-spacial']/a/text()")[0]
        dialog_list = soup.find_all(name='div', class_='context-left')
        dialog_str = ''
        for item in dialog_list:
            people = item.find(name='h6', class_='doctor-name').get_text()
            dialog = item.find(name='p').get_text().strip().replace("\n", '')
            dialog_str = dialog_str + people + ":" + dialog + "\n"

        return Dialog(
            inquiry_question_id=question_id,
            clinic_id=clinic_id,
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
            doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
            hospital_id = get_reg_hospital_id(str(hospital_id_list[i]))
            raw_available_status = xpath.xpath(
                f"//div[@class='doctor-list']/div[{i + 1}]/div[@class='avatar-wrap']/span/text()")
            if len(raw_available_status) > 0:
                available_status = 1
            else:
                available_status = 0

            recommend_doctor_datas.append(DoctorRecommend(
                doctor_id=doctor_id,
                hospital_id=hospital_id,
                clinic_id=clinic_id,
                recommend_doctor_is_inquiry=available_status
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
            doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
            hospital_id = get_reg_hospital_id(str(hospital_id_list[i]))
            recommend_doctor_datas.append(DoctorRecommend(
                doctor_id=doctor_id,
                hospital_id=hospital_id,
                clinic_id=clinic_id,
                recommend_doctor_is_inquiry=1
            ))
        return recommend_doctor_datas
    except Exception as e:
        logger.warning("科室 {} 页面解析错误, ".format(clinic_id))
        return None

@parse_decorator(False)
def clinic_html_2_doctor_base(clinic_id, html):
    '''
    【根据科室找医生】页面->医生基础信息（仅未爬过）
    :param clinic_id: 科室id
    :param html: response.text
    :return: 医生基础信息对象/None（错误）
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
    hospital_base_datas = []

    try:
        hospital_id_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[2]/a/@href")
        hospital_name_list = xpath.xpath("//div[@class='doctor-list']/div/div[@class='detail']/div[2]/a/text()")

        for i in range(len(hospital_id_list)):
            hospital_id = get_reg_hospital_id(str(hospital_id_list[i]))
            hospital_name = get_reg_clinic_name(str(hospital_name_list[i]))

            hospital_base_datas.append(Hospital(
                hospital_id=hospital_id,
                hospital_name=hospital_name
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

def anti_crawl_doctor_mid_frequency_status(doctor_id):
    return DoctorMidFrequencyStatus(
        doctor_id=doctor_id,
        is_reward_crawl=0,
    )

def anti_crawl_doctor_low_frequency_status(doctor_id):
    return DoctorLowFrequencyStatus(
        doctor_id=doctor_id,
        is_auth_crawl=0,
        is_description_crawl=0,
        is_tag_crawl=0
    )


