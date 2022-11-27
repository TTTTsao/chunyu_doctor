import json
from decimal import Decimal

from spider.db.models import *
from spider.page_get.basic import get_page_html
from spider.util.basic import trans_to_datetime
from spider.util.reg.reg_doctor import *
from spider.util.reg.reg_hospital import (get_reg_hospital_id, get_reg_clinic_id)


from lxml import etree

def get_active_doctor_base_info(html):
    '''
    get active doctor base info data
    从【根据科室找医生】获取活跃的医生基本信息
    :param html:
    :return:
    '''
    if not html:
        return

    xpath = etree.HTML(html)
    doctor_name_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/span[1]/text()")
    doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_base_info_datas = []

    for i in range(len(doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_name = get_reg_doctor_name(str(doctor_name_list[i]))

        doctor_base_info = DoctorBaseInfo()
        doctor_base_info.doctor_id = doctor_id
        doctor_base_info.doctor_name = doctor_name
        doctor_base_info_datas.append(doctor_base_info)

    return doctor_base_info_datas

def get_active_doctor_img(html):
    '''
    get active doctor img info data
    从【根据科室找医生】获取活跃的医生头像信息
    :param html:
    :return:
    '''
    if not html:
        return

    doctor_img_datas = []
    xpath = etree.HTML(html)
    doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_img_url_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[1]/a/img/@src")

    for i in range(len(doctor_id_list)):
        doctor_img = DoctorImg()

        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_img.doctor_id = doctor_id
        # print("doctor_id", doctor_id)

        doctor_img_url = str(doctor_img_url_list[i])
        doctor_img.doctor_img_remote_path = doctor_img_url
        # print("doctro_img_url", doctor_img_url)

        doctor_img_datas.append(doctor_img)

    return doctor_img_datas



def get_doctor_base_info(doctor_id, html):
    '''
    从医生页面获取基本信息
    :param html:
    :return: doctor base info 对象
    '''
    if not html:
        return

    doctor_base_info = DoctorBaseInfo()
    xpath = etree.HTML(html)

    doctor_base_info.doctor_id = doctor_id
    doctor_name = str(xpath.xpath('/html/body/div[4]/div[1]/div[1]/div/div[2]/div[1]/span[1]/text()')[0])
    doctor_base_info.doctor_name = doctor_name

    return doctor_base_info


def get_doctor_auth_info(doctor_id, html):
     '''
     从医生页面获取认证信息
     :param doctor_id:
     :param html:
     :return:
     '''
     if not html:
         return
     doctor_auth_info = DoctorAuthInfo()

     xpath = etree.HTML(html)

     doctor_auth_info.doctor_id = doctor_id
     hospital_id = xpath.xpath("/html/body/div[4]/div[1]/div[1]/div/div[2]/div[2]/a/@href")[0]
     clinic_id = xpath.xpath("/html/body/div[4]/div[1]/div[1]/div/div[2]/div[1]/a[1]/@href")[0]
     auth_grade = xpath.xpath("/html/body/div[4]/div[1]/div[1]/div/div[2]/div[1]/span[2]/text()")[0]
     auth_time = xpath.xpath("/html/body/div[5]/div/div[2]/div[3]/div[2]/text()")
     auth_status = xpath.xpath("/html/body/div[4]/div[1]/div[1]/div/div[2]/div[1]/span[3]/text()")[0]

     doctor_auth_info.doctor_auth_hospital_id = get_reg_hospital_id(str(hospital_id))
     doctor_auth_info.doctor_auth_clinic_id = get_reg_clinic_id(str(clinic_id))
     doctor_auth_info.doctor_auth_grade = str(auth_grade)
     doctor_auth_info.doctor_auth_time = get_reg_auth_time(str(auth_time))

     if str(auth_status) == "已认证":
         # print("判断一致")
         doctor_auth_info.doctor_auth_status = 1
     else:
         # print("判断不一致")
         doctor_auth_info.doctor_auth_status = 0

     return doctor_auth_info

def get_doctor_tag(doctor_id, html):
    '''
    从医生页面获取标签信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    doctor_tag = DoctorTag()
    xpath = etree.HTML(html)

    doctor_tag.doctor_id = doctor_id
    tag_content_dict = {}
    label_list = xpath.xpath("/html/body/div[4]/div[1]/div[1]/div/div[2]/div[3]/span/text()")
    # 判断有几个标签
    for i in range(len(label_list)):
        label_name = 'label'+str(i+1)
        tag_content_dict[label_name] = label_list[i]

    tag_content_json = json.dumps(tag_content_dict, ensure_ascii=False)
    doctor_tag.tag_content = tag_content_json
    return doctor_tag

def get_doctor_service_info(doctor_id, html):
    '''
    从医生页面获取服务信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    doctor_service_data = DoctorServiceInfo()
    doctor_service_data.doctor_id = doctor_id
    xpath = etree.HTML(html)

    serve_nums = xpath.xpath("/html/body/div[4]/div[1]/div[1]/ul/li[1]/span[1]/text()")[0]
    favorable_rate = xpath.xpath("/html/body/div[4]/div[1]/div[1]/ul/li[2]/span[1]/text()")[0]
    peer_recognization = xpath.xpath("/html/body/div[4]/div[1]/div[1]/ul/li[3]/span[1]/text()")[0]
    patient_praise_num = xpath.xpath("/html/body/div[4]/div[1]/div[1]/ul/li[4]/span[1]/text()")[0]
    followers = xpath.xpath("/html/body/div[4]/div[1]/div[2]/div[2]/text()")[0]

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

def get_doctor_price(doctor_id, html):
    '''
    从医生页面获取价格信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    doctor_price_data = DoctorPrice()
    doctor_price_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    price = xpath.xpath("/html/body/div[4]/div[1]/a/div[1]/span/text()")
    type = xpath.xpath("/html/body/div[4]/div[1]/a/div[1]/text()")
    discount = xpath.xpath("/html/body/div[4]/div[1]/a/span/text()")

    # 判断有无价格信息
    if len(price) == 0:
        doctor_price_data.doctor_price_type = '暂无问诊服务'
        # print(doctor_price_data.doctor_price_type)
    else:
        # 判断有无折扣信息
        if len(discount) == 0:
            # print('无折扣')
            doctor_price_data.doctor_price_type = get_reg_price_type(str(type[0]))
            doctor_price_data.doctor_price = Decimal(price[0])
        else:
            # print('有折扣')
            doctor_price_data.doctor_price_type = get_reg_price_type(str(type[0]))
            doctor_price_data.doctor_price = Decimal(price[0])
            doctor_price_data.doctor_price_discount = get_reg_price_discount(str(discount[0]))

    return doctor_price_data

def get_doctor_description(doctor_id, html):
    '''
    从医生页面获取个人简介信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    doctor_description_data = DoctorDescription()
    doctor_description_data.doctor_id = doctor_id

    xpath = etree.HTML(html)
    # TODO 增加页面元素判断，是否存在某某字段-先判断是否有4个，有3个（无专业擅长）再做详细判断
    # id号：3eee347e37efdc88b3b9、2e1b2ca0aacbd13104db

    temp_length = len(xpath.xpath("//p[@class='detail']"))
    if temp_length == 4:
        edu_backgroud = xpath.xpath("//p[@class='detail']/text()")[1]
        doctor_description_data.doctor_description_edu_background = get_reg_doctor_profile(str(edu_backgroud))

        major = xpath.xpath("//p[@class='detail']/text()")[3]
        doctor_description_data.doctor_description_major = get_reg_doctor_profile(str(major))

        description = xpath.xpath("//p[@class='detail']/text()")[5]
        doctor_description_data.doctor_description_description = get_reg_doctor_profile(str(description))

        hospital_location = xpath.xpath("//p[@class='detail']/text()")[7]
        doctor_description_data.doctor_description_hospital_location = get_reg_doctor_profile(str(hospital_location))
    elif temp_length == 3:
        edu_backgroud = xpath.xpath("///p[@class='detail']/text()")[1]
        doctor_description_data.doctor_description_edu_background = get_reg_doctor_profile(str(edu_backgroud))

        description = xpath.xpath("//p[@class='detail']/text()")[3]
        doctor_description_data.doctor_description_description = get_reg_doctor_profile(str(description))

        hospital_location = xpath.xpath("//p[@class='detail']/text()")[5]
        doctor_description_data.doctor_description_hospital_location = get_reg_doctor_profile(str(hospital_location))

    return doctor_description_data

def get_doctor_comment_label(doctor_id, html):
    '''
    从医生页面获取医生患者评价标签（id、4个评价标签的数量）
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return
    doctor_comment_label_data = DoctorCommentLabel()
    doctor_comment_label_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    label_num_list = xpath.xpath("/html/body/div[4]/ul[1]/li/span/text()")

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

def get_doctor_reward(doctor_id, html):
    '''
    从医生心意墙信息（id、打赏时间、打赏金额、打赏留言）
    :param doctor_id:
    :return:
    '''
    if not html:
        return
    xpath = etree.HTML(html)
    doctor_reward_datas = []
    reward_datetime_list = xpath.xpath("/html/body/div[4]/div[11]/ul/li/span/text()")
    reward_amount_list = xpath.xpath("/html/body/div[4]/div[11]/ul/li/div/span[1]/i/text()")
    reward_content_list = xpath.xpath("/html/body/div[4]/div[11]/ul/li/div/span[2]/text()")

    # 判断是否有【心意墙】板块
    if len(reward_content_list) == 0:
        # 警告日志：没有心意墙
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

def get_active_doctor_id_list(html):
    '''
    get active doctor id list
    从【根据科室找医生】获取活跃的医生id list
    :param html:
    :return:
    '''
    if not html:
        return

    xpath = etree.HTML(html)
    row_doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_id_list = []

    for i in range(len(row_doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(row_doctor_id_list[i]))
        doctor_id_list.append(doctor_id)

    return doctor_id_list

def get_doctor_base_info_from_clinic(html):
    '''
    get doctor base info from clinic page
    从科室详情页获取医生基本信息
    :param html:
    :return:
    '''
    if not html:
        return
    xpath = etree.HTML(html)

    doctor_id_list = xpath.xpath("//div[@class='avatar-wrap']/a/@href")
    doctor_name_list = xpath.xpath("//div[@class='detail']/div/a/span[1]/text()")

    # 判断页面有无医生
    if len(doctor_id_list) == 0:
        print("该科室没有医生")
        return

    doctor_base_info_datas = []
    for i in range(len(doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_name = get_reg_doctor_name(str(doctor_name_list[i]))

        doctor_base_info = DoctorBaseInfo()
        doctor_base_info.doctor_id = doctor_id
        doctor_base_info.doctor_name = doctor_name
        doctor_base_info_datas.append(doctor_base_info)

    return doctor_base_info_datas

def get_doctor_img_from_clinic(html):
    '''
    get doctor img info from clinic page
    从科室详情页获取医生头像信息
    :param html:
    :return:
    '''
    if not html:
        return
    xpath = etree.HTML(html)

    doctor_id_list = xpath.xpath("//div[@class='avatar-wrap']/a/@href")
    doctor_img_url_list = xpath.xpath("//div[@class='avatar-wrap']/a/img/@src")

    # 判断页面有无医生
    if len(doctor_id_list) == 0:
        print("该科室没有医生")
        return

    doctor_img_datas = []
    for i in range(len(doctor_id_list)):
        doctor_img = DoctorImg()

        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_img.doctor_id = doctor_id

        doctor_img_url = str(doctor_img_url_list[i])
        doctor_img.doctor_img_remote_path = doctor_img_url

        doctor_img_datas.append(doctor_img)

    return doctor_img_datas

def is_there_is_doctor(html):
    '''
    判断医生是否存在的情况
    :param html:
    :return:
    '''



if __name__ == '__main__':
    # # doctor_id = 'clinic_web_306c0a5afec5230f'
    # doctor_id = 'clinic_web_f9824e9871af1635'
    # url = 'https://www.chunyuyisheng.com/pc/doctor/clinic_web_306c0a5afec5230f/'
    url = 'https://chunyuyisheng.com/pc/clinic/00245b9d266dac6d-ab/'
    # url = 'https://chunyuyisheng.com/pc/doctors/'
    html = get_page_html(url)
    get_doctor_base_info_from_clinic(html)


