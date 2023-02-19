import re
from decimal import Decimal

def get_reg_auth_time(str):
    '''
    get reg auth time
    :param str:
    :return: auth time (Datetime)
    '''
    auth_time = re.search("(\d+年\d+月\d+日)", str).group()
    return auth_time


def get_reg_doctor_id(str):
    '''
    get reg doctor id
    :param str:
    :return: doctor id
    '''
    pattern = re.compile("/pc/doctor/")
    id_data = re.sub(pattern, '', str)
    doctor_id = re.sub("/$", '', id_data)
    return doctor_id

def get_reg_followers(str):
    '''
    get reg doctor's followers
    :param str:
    :return:
    '''
    followers = int(re.search("(\d+)", str).group())
    return followers

def get_reg_price_type(str):
    '''
    get reg price type
    :param str:
    :return:
    '''
    pattern = re.compile("\(")
    price_type = re.sub(pattern, '', str)
    return price_type

def get_reg_price_discount(str):
    '''
    get reg price discount
    :param str:
    :return:
    '''
    price_discount = Decimal(re.search("(\d)", str).group())
    return price_discount

def get_reg_label_num(str):
    '''
    get reg label num
    :param str:
    :return:
    '''
    label_num = int(re.search("(\d+)", str).group())
    return label_num

def get_reg_reward_amount(str):
    '''
    get reg reward amount
    :param str:
    :return:
    '''
    reward_amount = int(re.search("(\d+)", str).group())
    return reward_amount

def get_reg_doctor_profile(str):
    '''
    get reg doctor profile
    :param str:
    :return:
    '''
    front_pattern = re.compile("^(\s*)")
    front = re.sub(front_pattern, '', str)
    end_pattern = re.compile("(\s*)$")
    profile = re.sub(end_pattern, '', front)
    return profile

def get_reg_doctor_name(str):
    '''
    get reg doctor name
    :param str:
    :return:
    '''
    pattern = re.compile('\\\\+\w{3}')
    doctor_name = re.sub(pattern, '', str)
    return doctor_name

def get_reg_mobile_price(str):
    pattern = re.compile('图文咨询¥')
    price = int(re.sub(pattern, '', str))
    return price

if __name__ == '__main__':
    row_doctor_id = '/pc/doctor/clinic_web_fa2e2aadbeb99583/'
    row_auth_time = '该医生已于2017年09月15日提交信息并通过认证审核。'
    row_followers = '已有563人关注'
    row_price_type = "图文咨询("
    row_price_discount = '新用户享4折¥16.0'
    row_label_num = '[285]'
    row_reward_amount = '36元'
    doctor_name = "YAN ZI\xa0"
    price = '图文咨询¥-1'
    print(get_reg_mobile_price(price))


