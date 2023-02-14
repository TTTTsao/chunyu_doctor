import requests

from spider.config.conf import get_open_proxy_url
from spider.util.proxy.base_proxy import ProxyPool, Proxy

url = get_open_proxy_url()

def getIP():
    return {
        'http' : requests.get(url).text,
        'https' : requests.get(url).text
    }