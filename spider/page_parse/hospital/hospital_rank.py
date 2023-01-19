from lxml import etree

from spider.page_get.basic import get_page_html

HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'
HOSPITAL_CLINIC_URL = 'https://chunyuyisheng.com/pc/clinic/{}'
HOSPITAL_RANK_URL = 'https://chunyuyisheng.com//pc/hospitallist/{}/{}'

def get_hospital_rank(location_id, clinic_id, is_second_page = False):
    '''

    :param location_id:
    :param clinic_id:
    :param is_second_page:
    :return: hospital_rank info data
    '''
    url = HOSPITAL_CLINIC_URL.format(location_id, clinic_id)
    html = get_page_html(url)
    xpath = etree.HTML(html)

    area = str(xpath.xpath('/html/body/div[4]/section[1]/div[1]/ul/li[2]/a/text()'))
    province = str(xpath.xpath('/html/body/div[4]/section[1]/div[1]/ul/li[3]/a/text()'))
    # TODO 判断province是否为空
    city = str(xpath.xpath('/html/body/div[4]/section[1]/div[1]/ul/li[4]/a/text()'))
    # TODO 判断city是否为空

    # TODO 选取当前selected的一级科室

    # TODO 判断是否为二级科室排名页面

    # TODO 写入 hospital rank info data 对象

    # TODO 返回 hospital rank info data 对象

    pass