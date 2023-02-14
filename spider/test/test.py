import datetime

from spider.page_get.chunyu_request.doctor_page_request import get_doctor_moblie_detail_page
from spider.page_parse.field_parse.doctor_parse import *
from spider.page_parse.basic import is_mobile_price_exist

# url = 'https://m.chunyuyisheng.com/m/doctor/clinic_web_2f8e3f26201fe950/'
# doctor_id = 'clinic_web_2f8e3f26201fe950'
url = 'https://m.chunyuyisheng.com/m/doctor/clinic_web_b1801427139dfa78/'
doctor_id = 'clinic_web_b1801427139dfa78'

if __name__ == '__main__':
    html = get_doctor_moblie_detail_page(doctor_id)
    print(doctor_mobile_page_html_2_doctor_service_info(doctor_id, html))
