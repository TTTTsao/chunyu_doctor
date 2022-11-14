import requests
from requests.adapters import HTTPAdapter

from spider.page_get.clinic_basic import get_clinic_html
from spider.page_parse.clinic import get_first_clinic_id_list
from spider.page_parse.clinic import get_first_clinic_list
from spider.page_parse.clinic import is_second_clinic_exist
from spider.page_parse.clinic import get_second_clinic_list

BASE_URL = 'https://chunyuyisheng.com/pc/doctors/0-0-0/'
CLINIC_URL = 'https://chunyuyisheng.com/pc/doctors/{}/'


# 抓取一级科室
def crawl_all_first_clinic():
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    first_clinic_html = get_clinic_html(BASE_URL)
    first_clinic_info = get_first_clinic_list(first_clinic_html)

    # 插入数据库


    pass


# 抓取二级科室
def crawl_all_second_clinic():
    # Start crawl and 开始爬虫-日志
    # crawler.info('the crawling url is {url}'.format(url=url))

    # 循环遍历一级科室页面查探是否有二级科室
    first_clinic_id_list = get_first_clinic_id_list(BASE_URL)
    second_clinic_info = get_second_clinic_list(first_clinic_id_list)

    # 插入数据库


    pass


if __name__ == '__main__':
    # try:
    #     session = requests.Session()
    #     session.mount('http://', HTTPAdapter(max_retries=3))
    #     session.mount('https://', HTTPAdapter(max_retries=3))
    #     session.keep_alive = False
    #     r = requests.get(base_url, headers={'Connection': 'close'}, timeout=20, verify=False)
    #     print(r.text)
    #     r.close()
    # except:
    #     print('========出现错误==========')
    #     r = requests.get(base_url, headers={'Connection': 'close'}, timeout=20, verify=False)
    #     print("requests.status.code", r.status_code)
    pass
