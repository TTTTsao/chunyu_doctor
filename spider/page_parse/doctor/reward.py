from spider.db.models import DoctorReward
from spider.util.basic import trans_to_datetime
from spider.util.reg.reg_doctor import get_reg_reward_amount
from spider.decorators.parse_decorator import parse_decorator
from spider.page_parse.basic import is_doctor_detail_page_right
from loguru import logger
from lxml import etree

@parse_decorator(False)
def get_doctor_reward(doctor_id, html):
    '''
    从医生心意墙信息（id、打赏时间、打赏金额、打赏留言）
    :param doctor_id:
    :return:
    '''
    if not html:
        return False
    if not is_doctor_detail_page_right(doctor_id, html):
        logger.error("被反爬，{} 医生详情页面与医生不一致".format(doctor_id))
        # TODO 增加将未成功爬取的doctor_id 写入一个json文件 用于后续爬取
        return False
    xpath = etree.HTML(html)
    doctor_reward_datas = []
    try:
        reward_datetime_list = xpath.xpath("//ul[@class='money-list ']/li/span/text()")
        reward_amount_list = xpath.xpath("//ul[@class='money-list ']/li/div/span[1]/i/text()")
        reward_content_list = xpath.xpath("//ul[@class='money-list ']/li/div/span[2]/text()")
    except Exception:
        return False

    # 判断是否有【心意墙】板块
    if len(reward_content_list) == 0:
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