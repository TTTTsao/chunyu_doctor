from spider.decorators.parse_decorator import parse_decorator
from loguru import logger

@parse_decorator(False)
def is_404(html):
    try:
        # doctor detail info is deleted
        if '抱歉，你所访问的网页不存在了，请返回主页' in html:
            return True
        elif html == '':
            return True
        else:
            return False
    except AttributeError:
        return False

@parse_decorator(False)
def is_page_has_no_doctor_nums(html, clinic_doctor_nums):
    try:
        if '暂无相关信息' in html:
            logger.warning("该页面暂无医生相关信息")
            return True
        elif len(clinic_doctor_nums) == 0:
            logger.warning("该页面无人数板块")
            return True
        elif int(clinic_doctor_nums[0]) == 0:
            logger.warning("该科室页面人数为0")
            return True
        elif is_404(html):
            return True
    except AttributeError:
        return False

