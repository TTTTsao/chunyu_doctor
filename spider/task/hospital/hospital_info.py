

from spider.page_get.basic import get_page_html
from spider.page_parse.hospital import (get_hospital_province_list,
                                        get_hospital_list_from_province,
                                        )

BASE_URL = 'https://chunyuyisheng.com/pc/hospitals/'
HOSPITAL_URL = 'https://chunyuyisheng.com/pc/hospitals/{}'
HOSPITAL_DETAIL_URL = 'https://chunyuyisheng.com/pc/hospital/{}'

def crawl_all_hospital_base_info():
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    # 获取所有省份id：get_hospital_province_list

    # 遍历获得每个省份下的医院id：get_hospital_list_from_province

    # 进入每个医院详情页

    # 将数据存入数据库


    pass

# 根据hospital_id爬取医院信息
def crawl_hospital_base_info(hospital_id, city):
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    url = HOSPITAL_DETAIL_URL.format(hospital_id)
    html = get_page_html(url)

    # 获取
    id = hospital_id
    name = ''


    pass