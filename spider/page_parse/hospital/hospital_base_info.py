import json

from lxml import etree

from spider.util.reg.reg_hospital import get_reg_hospital_profile
from spider.db.models import Hospital

def get_hospital_base_info(hospital_id, city, html):
    '''
    get hospital base info from detail page
    :param html:
    :return: hospital_base_info data
    '''
    if not html: return
    hospital_data = Hospital()
    xpath = etree.HTML(html)

    hospital_data.hospital_id = hospital_id
    hospital_data.hospital_city = city
    name = (xpath.xpath('/html/body/div[4]/div[1]/h3/text()'))[0]
    hospital_data.hospital_name = str(name)

    area = (xpath.xpath('//*[@id="region_href"]/text()'))[0]
    hospital_data.hospital_area = str(area)

    province = (xpath.xpath('/html/body/div[4]/ul[1]/li[3]/a/text()'))[0]
    hospital_data.hospital_province = str(province)

    row_profile = xpath.xpath("//div[@class='content-info']/div[1]/p/text()")
    str_profile = str(row_profile)
    hospital_data.hospital_profile = get_reg_hospital_profile(str_profile)

    # JSON-tag
    tag_dic = {}
    tag_dic["rank"] = xpath.xpath("/html/body/div[4]/div[1]/span[1]/text()")[0]
    tag_dic["type"] = xpath.xpath("/html/body/div[4]/div[1]/span[2]/text()")[0]
    hospital_data.hospital_tag = json.dumps(tag_dic, ensure_ascii=False)  # ensure_ascii=False 防止中文被转化

    return hospital_data