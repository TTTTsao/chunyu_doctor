from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.illness import *
from spider.db.dao.doctor_dao import DoctorIllnessOper
from spider.logger import crawler, storage

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'
ILLNESS_BASE_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}/qa/?is_json=1&tag=&page_count=20&page=1'
ILLNESS_AJAX_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}/qa/?is_json=1&page_count=20&page={}&tag={}'

def crawl_illness_question(doctor_id):
    '''
    TODO 抓取医生好评问题信息（dr_id、ques_id、clinic_id、type、time、title、detail_html）
    （通过ajax请求抓取）
    :param doctor_id:
    :return:
    '''
    # 1.通过ajax的json获取【所有问题类型列表】
    # 2.遍历不同类型的ajax请求并翻页（翻页需要判断 1.是否返回的json对象为空 2.是否返回的问题数量<20 ）
    # 3.data的不同属性抓取在json中和detail_url中
    url = ILLNESS_BASE_URL.format(doctor_id)
    html = get_page_html(url)

    if is_illness_none(html):
        # 判断hot_consults数据是否为空，为空直接返回
        return
    hot_consults = get_illness_hot_consults(html)
    for type in hot_consults:
        cur_page = 1
        flag = True
        while flag:
            # 2.has_more_page是否为True，为True进行翻页操作（flag = has_more_page(html)）
            cur_url = ILLNESS_AJAX_URL.format(doctor_id, cur_page, type)
            cur_html = get_page_html(cur_url)
            illness_datas = get_illness_datas(doctor_id, type, cur_html)

            # 不存在
            if not illness_datas:
                # TODO 日志警告
                return

            if not DoctorIllnessOper.get_doctor_illness_by_doctor_id(doctor_id):
                # TODO 插入日志：新增
                DoctorIllnessOper.add_all(illness_datas)
            else:
                # TODO 日志：已存在并更新
                DoctorIllnessOper.add_all(illness_datas)

            cur_page += 1
            flag = has_more_page(cur_html)
