from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.reward import get_doctor_reward

from spider.db.dao.doctor_dao import DoctorRewardOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

def crawl_doctor_reward(doctor_id):
    '''
    抓取医生心意墙信息（id、打赏时间、打赏金额、打赏留言）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    # TODO crawl-info 正在抓取xx医生心意墙信息
    # crawler.info('the crawling url is {url}'.format(url=url))
    doctor_reward_data = get_doctor_reward(doctor_id, html)
    # 不存在
    if not doctor_reward_data:
        # TODO parse-waring 日志警告 不存在心意墙信息
        return

    if not DoctorRewardOper.get_doctor_reward_by_doctor_id(doctor_id):
        # TODO storage-info 插入日志：新增
        DoctorRewardOper.add_all(doctor_reward_data)
    else:
        # TODO storage-info 日志：已存在并更新
        DoctorRewardOper.add_all(doctor_reward_data)
    # TODO storage-error 日志-插入失败