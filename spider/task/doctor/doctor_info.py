
BASE_URL = 'https://chunyuyisheng.com/pc/doctors/0-0-0/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
DOCTOR_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

# TODO 抓取所有医生的基本信息（id、name）
def crawl_all_doctor_base_info():
    pass

# TODO 抓取所有医生的头像信息（id，remote_url）
def crawl_all_doctor_img():
    pass

# TODO 抓取所有医生详情页信息（认证信息、标签信息、服务信息、价格信息、简介信息、好评信息、心意墙信息）
def crawl_all_doctor_detail_info():
    pass

# TODO 抓取医生认证信息（id、认证状态、医院id、科室id、职称、认证时间）
def crawl_doctor_auth_info():
    pass

# TODO 抓取医生标签信息（id、tag【JSON形式存储】）
def crawl_doctor_tag():
    pass

# TODO 抓取医生服务信息（id、服务人次、好评率、同行认可、患者心意、关注人数）
def crawl_doctor_service_info():
    pass

# TODO 抓取医生价格信息（id、教育背景、专业擅长、个人简介、医院地点）
def crawl_doctor_price():
    pass

# TODO 抓取医生患者评价标签（id、4个评价标签的数量）
def crawl_doctor_comment_label():
    pass

# TODO 抓取医生好评问题信息（dr_id、ques_id、clinic_id、type、time、title、detail_html）
#  （通过ajax请求抓取）
def crawl_illness_question():
    pass

# TODO 抓取医生心意墙信息（id、打赏时间、打赏金额、打赏留言）
def crawl_doctor_reward():
    pass