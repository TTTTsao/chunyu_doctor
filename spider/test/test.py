import datetime

from spider.page_get.chunyu_request.doctor_page_request import *
from spider.page_parse.field_parse.doctor_parse import *
from spider.page_parse.basic import is_mobile_price_exist

# url = 'https://m.chunyuyisheng.com/m/doctor/clinic_web_2f8e3f26201fe950/'
# doctor_id = 'clinic_web_2f8e3f26201fe950'
url = 'https://www.chunyuyisheng.com/pc/doctor/clinic_web_fa2e2aadbeb99583/'
doctor_id = 'clinic_web_fa2e2aadbeb99583'
question_url = 'https://www.chunyuyisheng.com/pc/qa/7Lh-cJaXAolrr18G0TXYfw/'
question_id = '7Lh-cJaXAolrr18G0TXYfw'

if __name__ == '__main__':
    html = get_doctor_inquiry_detail_page(question_id)
    soup = BeautifulSoup(html, 'lxml')
    dialog_list = soup.find_all(name='div', class_='context-left')
    dialog_str = ''
    for item in dialog_list:
        people = item.find(name='h6', class_='doctor-name').get_text()
        dialog = item.find(name='p').get_text().strip()
        dialog_str = dialog_str + people + ":" + dialog + "\n"
    print(dialog_str)



