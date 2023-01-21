from decimal import Decimal

from spider.db.models import DoctorPrice
from spider.util.reg.reg_doctor import (get_reg_price_type, get_reg_price_discount)
from spider.decorators.parse_decorator import parse_decorator

from lxml import etree

@parse_decorator(False)
def get_doctor_price(doctor_id, html):
    '''
    从医生页面获取价格信息
    :param doctor_id:
    :param html:
    :return:
    '''
    if not html:
        return False
    doctor_price_data = DoctorPrice()
    doctor_price_data.doctor_id = doctor_id
    xpath = etree.HTML(html)
    try:
        price = xpath.xpath("/html/body/div[4]/div[1]/a/div[1]/span/text()")
        price_type = xpath.xpath("/html/body/div[4]/div[1]/a/div[1]/text()")
        discount = xpath.xpath("/html/body/div[4]/div[1]/a/span/text()")
    except Exception as e:
        return False

    # 判断有无价格信息
    if len(price) == 0: doctor_price_data.doctor_price_type = '暂无问诊服务'
    else:
        # 判断有无折扣信息
        if len(discount) == 0:
            doctor_price_data.doctor_price_type = get_reg_price_type(str(price_type[0]))
            doctor_price_data.doctor_price = Decimal(price[0])
        else:
            doctor_price_data.doctor_price_type = get_reg_price_type(str(price_type[0]))
            doctor_price_data.doctor_price = Decimal(price[0])
            doctor_price_data.doctor_price_discount = get_reg_price_discount(str(discount[0]))

    return doctor_price_data
