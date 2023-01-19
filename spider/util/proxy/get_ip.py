import requests

from spider.config.conf import get_proxy_url

url = get_proxy_url()

def getIP():
    return {
        'http' : requests.get(url).text,
        'https' : requests.get(url).text
    }