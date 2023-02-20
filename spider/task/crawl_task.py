import time
import queue
import threading
import json
import random
import signal

from sqlalchemy import text
from concurrent.futures import ThreadPoolExecutor

from spider.task.mapping_task.doctor_page_mapping import *
from spider.task.mapping_task.hospital_page_mapping import *
from spider.page_parse.field_parse.doctor_parse import *
from spider.db.basic import db_session
from spider.util.log_util import create_crawl_logger
logger = create_crawl_logger()
logger.remove()


all_done = False
exited = False

task_queue_dict = {
    "doctor_base": queue.Queue(),
    "doctor_status": queue.Queue(),
    "doctor_auth_des_tag": queue.Queue(),
    "doctor_price_comment": queue.Queue(),
    "doctor_reward": queue.Queue(),
    "doctor_question": queue.Queue(),
    "question_html": queue.Queue(),
    "recommend_doctor": queue.Queue(),
    "hospital": queue.Queue(),
    "hospital_rank": queue.Queue(),
    "inquiry_doctor_nums": queue.Queue()
}


def sig_handler(sig, frame):
    global exited
    exited = True
    logger.info('收到信号 signal %d, exited=%d' % (sig, exited))

def init_queue(queue_name, sql, session):
    logger.info("爬虫任务 {} 开始初始化队列".format(queue_name))
    result = session.execute(sql)
    for item in result:
        task_queue_dict[queue_name].put(item[0])
    logger.info("爬虫任务 {} 初始化队列成功，需要爬取数据量为 {}".format(queue_name, task_queue_dict[queue_name].qsize()))


def task_action(key_name, e_id):
    logger.info("爬虫任务 %s, id: %s 执行" % (key_name, e_id))
    if key_name == "recommend_doctor":
        recommend_doctor_mapping(e_id)
    if key_name == "doctor_status":
        doctor_detail_page_status_mapping(e_id, 24*30)
    if key_name == "anti_crawl_doctor_status":
        doctor_anti_crawl_detail_page_status_mapping(e_id)
    if key_name == "doctor_price_comment":
        doctor_high_frequency_info_mapping(e_id)
    if key_name == "doctor_auth_des_tag":
        doctor_low_frequency_info_mapping(e_id)
    if key_name == "doctor_question":
        doctor_question_mapping(e_id)
    if key_name == "question_html":
        question_html_mapping(e_id)
    if key_name == "inquiry_doctor_nums":
        hospital_high_frequency_mapping(e_id)


def task_run(done_list, task_queue, thread_order):
    time.sleep(thread_order)
    while not is_all_done(done_list, task_queue, thread_order):
        for k, v in task_queue.items():
            if not v.empty():
                done_list[thread_order] = False
                try:
                    got_id = v.get(block=False)
                except queue.Empty:
                    continue
                try:
                    task_action(k, got_id)
                except Exception as e:
                    logger.exception(e)


def is_all_done(done_list, task_queue, thread_order):
    if exited:
        return True
    for v in task_queue.values():
        if not v.empty():
            return False
    done_list[thread_order] = True
    for item in done_list:
        if not item:
            time.sleep(5)
            return False
    global all_done
    all_done = True
    return True

def __common_thread_task(thread_nums, queue_name, sql):
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    session = db_session
    pool = ThreadPoolExecutor(max_workers=thread_nums)
    done_list = [False for _ in range(thread_nums)]
    init_queue(queue_name=queue_name, sql=sql, session=session)
    start_time = time.time()
    for i in range(thread_nums):
        pool.submit(task_run, done_list, task_queue_dict, i)
    while not all_done and not exited:
        time.sleep(random.uniform(10, 20))
    pool.shutdown(wait=True)
    end_time = time.time()
    logger.info("爬虫任务 {} exit, 用时: {}".format(queue_name, end_time-start_time))


def crawl_recommend_doctor_task():
    '''
    抓取【科室页面-每日推荐医生】
    '''
    thread_nums = 1
    sql = text("""select distinct clinic_id from raw_clinic""")
    __common_thread_task(thread_nums=thread_nums, queue_name="recommend_doctor", sql=sql)

def crawl_doctor_status_task():
    '''
    抓取【医生页面状态】
    :return:
    '''
    thread_nums = 8
    sql = text("""
    SELECT DISTINCT b.doctor_id FROM raw_doctor_base_info AS b WHERE NOT EXISTS ( SELECT 1 FROM estimate_doctor_crawl_status AS a WHERE b.doctor_id=a.doctor_id LIMIT 0, 1 )
    """)
    __common_thread_task(thread_nums=thread_nums, queue_name="doctor_status", sql=sql)

def crawl_doctor_anti_status_task():
    '''
    抓取【被反爬医生页面状态】
    :return:
    '''
    thread_nums = 8
    sql = text("""select distinct doctor_id from estimate_doctor_crawl_status where is_anti_crawl=0""")
    __common_thread_task(thread_nums=thread_nums, queue_name="anti_crawl_doctor_status", sql=sql)

def crawl_doctor_high_fruency_info_task():
    '''
    抓取【医生高频更新信息：price、comment_label】
    :return:
    '''
    thread_nums = 16
    sql = text("""select distinct doctor_id from estimate_doctor_crawl_status where is_price_exist=1""")
    __common_thread_task(thread_nums=thread_nums, queue_name="doctor_price_comment", sql=sql)

def crawl_doctor_low_fruency_info_task():
    '''
    抓取【医生低频更新信息：auth、tag、description】
    :return:
    '''
    thread_nums = 10
    sql = text("""
    SELECT distinct A.doctor_id FROM estimate_doctor_crawl_status A WHERE (SELECT COUNT(1) AS num FROM raw_doctor_auth_info B WHERE A.doctor_id = B.doctor_id and A.is_page_404=1 )=0 LIMIT 100000
    """)
    __common_thread_task(thread_nums=thread_nums, queue_name="doctor_auth_des_tag", sql=sql)


def crawl_doctor_question_task():
    '''
    抓取【医生问诊对话详情信息（ajax）】
    :return:
    '''
    thread_nums = 2
    sql = text("""
SELECT DISTINCT b.doctor_id FROM raw_doctor_base_info AS b WHERE NOT EXISTS ( SELECT 1 FROM (SELECT DISTINCT doctor_id FROM raw_html_illness) AS a WHERE b.doctor_id=a.doctor_id LIMIT 0, 1 )    """)
    __common_thread_task(thread_nums=thread_nums, queue_name="doctor_question", sql=sql)

def crawl_question_html_task():
    '''
    抓取【医生问诊对话详情html信息（html）】
    :return:
    '''
    thread_nums = 1
    sql = text("""select distinct illness_question_id from raw_html_illness where illness_detail_html is null or illness_detail_html=0""")
    __common_thread_task(thread_nums=thread_nums, queue_name="question_html", sql=sql)


def crawl_realtime_inquiry_task():
    '''
    抓取【医院实时可咨询医生数信息】
    :return:
    '''
    thread_nums = 8
    sql = text("""select distinct hospital_id from raw_hospital""")
    __common_thread_task(thread_nums=thread_nums, queue_name="inquiry_doctor_nums", sql=sql)


if __name__ == '__main__':
    crawl_recommend_doctor_task()
    # crawl_doctor_status_task()
    # crawl_doctor_question_task()
    # crawl_question_html_task()
    # crawl_doctor_high_fruency_info_task()