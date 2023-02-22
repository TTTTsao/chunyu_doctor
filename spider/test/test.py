import datetime
import re

from spider.page_get.chunyu_request.doctor_page_request import *
from spider.page_parse.field_parse.doctor_parse import *
from spider.page_parse.basic import *

# url = 'https://m.chunyuyisheng.com/m/doctor/clinic_web_2f8e3f26201fe950/'
# doctor_id = 'clinic_web_2f8e3f26201fe950'
url = 'https://www.chunyuyisheng.com/pc/doctor/clinic_web_fa2e2aadbeb99583/'
doctor_id = 'clinic_web_fa2e2aadbeb99583'
question_url = 'https://www.chunyuyisheng.com/pc/qa/6VVj_4YDKPEkKYbYAYoq0A/'
question_id = '6VVj_4YDKPEkKYbYAYoq0A'

if __name__ == '__main__':
    html = get_doctor_inquiry_detail_page(question_id)
    print(is_illness_detail_page_right(question_id, html))
    # soup = BeautifulSoup(html, 'lxml')
    # clinic_name = soup.find(name='div', class_="bread-crumb-spacial").find(name='a').get_text()
    # print("clinic_name", clinic_name)
    # dialog_list = soup.find_all(name='div', class_='context-left')
    # dialog_str = ''
    # for item in dialog_list:
    #     people = item.find(name='h6', class_='doctor-name').get_text()
    #     dialog = item.find(name='p').get_text().strip().replace("\n", '')
    #     dialog_str = dialog_str + people + "：" + dialog + "\n"
    # print(dialog_str)
    # print("总对话次数为", dialog_str.count("\n"), "次")
    # print("患者发送次数为", dialog_str.count("患者："), "次")
    # print("医生发送次数为", dialog_str.count("医生："), "次")
    # print("图片交流次数", dialog_str.count("图片因隐私问题无法显示"))
    # print("音频交流次数", dialog_str.count("audio"))
    # # 判断回复类型中是否存在文字/音频/图片
    # count_list = dialog_str.split("\n")
    # print("最后回复人及内容", count_list[len(count_list)-2])
    # for item in count_list:
    #     if "医生：" in item and "audio" not in item and "图片因隐私问题无法显示" not in item:
    #         # 判断医生回复中是否存在【图片】和【音频】类型
    #         print(item)
    #         str_num = item.split("：")[1]
    #         print(len(str_num), str_num)






