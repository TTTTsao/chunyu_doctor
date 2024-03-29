import os
import random

import yaml
from yaml import load

config_path = os.path.join(os.path.dirname(__file__), 'spider.yaml')

with open(config_path, encoding='utf-8') as f:
    cont = f.read()

cf = load(cont, Loader=yaml.CLoader)

def get_timeout():
    return cf.get('time_out')

def get_crawl_interal():
    interal = random.randint(cf.get('min_crawl_interal'), cf.get('max_crawl_interal'))
    return interal

def get_excp_interal():
    return cf.get('excp_interal')

def get_max_retries():
    return cf.get("max_retries")

def get_db_args():
    return cf.get('db')

def get_max_home_page():
    return cf.get('max_home_page')

def get_open_proxy_url():
    return cf.get('JHao-proxy_url')

def get_logger_logging_format():
    return cf.get('logging_format')

def get_thread_nums():
    return cf.get('thread_nums')

def get_frequency_limit():
    return cf.get("frequency_limit")

def get_usage_limit():
    return cf.get("usage_limit")

def get_choose_proxy():
    return cf.get("proxy_url")