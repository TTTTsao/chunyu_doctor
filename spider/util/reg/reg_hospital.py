import re

def get_reg_hospital_id(str):
    '''
    use re to get hospital id
    :param str:
    :return: hospital id
    '''
    pattern = re.compile("/pc/hospital/")
    id_data = re.sub(pattern, '', str)
    hospital_id = re.sub("/$", '', id_data)
    return hospital_id

def get_reg_clinic_rank_id(str):
    '''
    use re to get clinic rank id
    :param str:
    :return: clinc_rank_id
    '''
    pattern = '/pc/hospitallist/0/'
    clinc_rank_id = re.sub(pattern, '', str)
    return clinc_rank_id

def get_reg_clinic_name(str):
    '''
    use re to get clinic name
    :param str:
    :return:
    '''
    pattern = '([\u4e00-\u9fa5]+)'
    clinic_name = re.search(pattern, str).group()
    return clinic_name

def get_reg_province_id(str):
    '''
    use re to get province id
    :param str:
    :return: province id
    '''
    pattern = '([\d+]+-[\d])'
    province_id = re.search(pattern, str).group()
    return province_id

def get_reg_hospital_profile(str):
    '''
    use re to get hospital profile
    :param str:
    :return: hospital profile
    '''
    front_pattern = re.compile("^[\S{10}]+[\s*]+[\S*]+[\s*]+[\S*]+[\s*]+[\s*]")
    front_reg = re.sub(front_pattern, '', str)
    mid_pattern = re.compile('[\']+[,]+[\s]+[\']+[\\\\]+[u3000]+[\\\\]+[u3000]+[\d]*')
    mid_reg = re.sub(mid_pattern, '', front_reg)
    end_pattern = re.compile("\\\\+n+[\s*]+[\S*]+']$")
    end_reg = re.sub(end_pattern, '', mid_reg)
    return end_reg

def get_reg_clinic_id(str):
    '''
    use re to get clinic id
    :param str:
    :return: clinic id
    '''
    pattern = re.compile("/pc/clinic/")
    id_data = re.sub(pattern, '', str)
    clinic_id = re.sub("/$", '', id_data)
    return clinic_id

def get_reg_rank_name(str):
    '''
    use re to get rank name
    :param str:
    :return: rank name
    '''
    pattern = re.compile('[排名第]+[\d]*$')
    rank_name = re.sub(pattern, '', str)
    return rank_name

def get_reg_rank_level(str):
    '''
    use re to get rank level
    :param str:
    :return: rank level(int)
    '''
    rank_level = int(re.search('(\d)*$', str).group())
    return rank_level

def get_reg_clinic_profile(str):
    '''
    use re to get clinic profile
    :param str:
    :return: clinic profile
    '''
    front_pattern = re.compile("^[\S{10}]+[\s*]+[\S*]+[\s]*")
    front_reg = re.sub(front_pattern, '', str)
    mid_pattern = re.compile('[\']+[,]+[\s]+[\']+[\\\\]+[u3000]+[\\\\]+[u3000]+[\d]*')
    mid_reg = re.sub(mid_pattern, '', front_reg)
    end_pattern = re.compile("\\\\+n+[\s*]+[\S*]+']$")
    end_reg = re.sub(end_pattern, '', mid_reg)
    return end_reg