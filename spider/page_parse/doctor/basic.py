from spider.util.reg.reg_doctor import get_reg_doctor_id
from spider.decorators.parse_decorator import parse_decorator

from lxml import etree
import sys
from loguru import logger

from spider.config.conf import get_logger_logging_format
logging_format = get_logger_logging_format()

logger.add(sys.stderr, level="INFO", format=logging_format)
logger.add('spider/logs/parse_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/parse_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/parse_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')


@parse_decorator(False)
def get_active_doctor_id_list(html):
    '''
    get active doctor id list
    从【根据科室找医生】获取活跃的医生id list
    :param html:
    :return:
    '''
    if not html:
        return

    xpath = etree.HTML(html)
    row_doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_id_list = []

    for i in range(len(row_doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(row_doctor_id_list[i]))
        doctor_id_list.append(doctor_id)

    return doctor_id_list

@parse_decorator(False)
def get_doctor_id_list_from_clinic_page(html):
    '''
    从科室页获取当页的doctor id list
    :param html:
    :return:
    '''
    if not html:
        return
    xpath = etree.HTML(html)
    try:
        row_doctor_id_list = xpath.xpath("//div[@class='avatar-wrap']/a/@href")
    except Exception as e:
        logger.error("获取当前的科室页面的医生id列表失败，详情：{}".format(e))
        return False

    # 判断页面有无医生
    if len(row_doctor_id_list) == 0:
        logger.warning("该科室页面没有医生")
        return

    doctor_id_list = []
    for i in range(len(row_doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(row_doctor_id_list[i]))
        doctor_id_list.append(doctor_id)

    return doctor_id_list