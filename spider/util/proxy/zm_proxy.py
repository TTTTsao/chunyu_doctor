import requests
from spider.util.proxy.base_proxy import ProxyPool, Proxy
from spider.config.conf import get_max_retries

num = 1
HTTP_port = 1
HTTPS_port = 11
pack = 292585
time = 1

http_url = f'http://http.tiqu.letecs.com/getip3?num={num}&type=2&pro=0&city=0&yys=0&port={HTTP_port}&pack={pack}&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
https_url = f'http://http.tiqu.letecs.com/getip3?num={num}&type=2&pro=0&city=0&yys=0&port={HTTPS_port}&pack={pack}&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

max_retries = get_max_retries()

def __check_discard(proxy):
    return proxy.bad_request >= max_retries / 3

def __fetch_proxy():
    http_response = requests.get(url=http_url).json()["data"][0]
    https_response = requests.get(url=https_url).json()["data"][0]
    proxies = {
        "http": "http://%(host)s:%(port)s" % {"host": http_response["ip"], "port":https_response["port"]},
        "https": "https://%(host)s:%(port)s" % {"host": https_response["ip"], "port": https_response["port"]}
    }
    return proxies

def get_proxy(old_key):
    return ProxyPool.get_proxy(old_key, __fetch_proxy, __check_discard)


def request_success(key):
    ProxyPool.request_success(key)