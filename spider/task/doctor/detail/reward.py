from spider.page_get.basic import get_page_html
from spider.page_parse.doctor.reward import get_doctor_reward
from spider.decorators.crawl_decorator import crawl_decorator
from loguru import logger

from spider.db.dao.doctor_dao import DoctorRewardOper

DOCTOR_URL = 'https://www.chunyuyisheng.com/pc/doctor/{}'

@crawl_decorator
def crawl_doctor_reward(doctor_id):
    '''
    抓取医生心意墙信息（id、打赏时间、打赏金额、打赏留言）
    :param doctor_id:
    :return:
    '''
    url = DOCTOR_URL.format(doctor_id)
    html = get_page_html(url)
    logger.info("正在抓取 {} 医生的心意墙信息".format(doctor_id))
    doctor_reward_data = get_doctor_reward(doctor_id, html)
    # 不存在
    if not doctor_reward_data:
        logger.warning("{} 医生不存在心意墙信息".format(doctor_id))
        return

    DoctorRewardOper.add_all(doctor_reward_data)