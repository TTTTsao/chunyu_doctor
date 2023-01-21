import sys
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
import time
import queue
import threading
import json
import signal

from spider.task.doctor.detail.price import crawl_doctor_price
from spider.task.doctor.detail.service_info import crawl_doctor_service_info
from spider.task.doctor.detail.reward import crawl_doctor_reward
from spider.task.doctor.detail.comment_label import crawl_doctor_comment_label
from spider.task.doctor.detail.illness import crawl_illness_question
from spider.task.hospital.detail.real_time_inquiry import crawl_hospital_real_time_inquiry
from spider.config.conf import (get_logger_logging_format, get_thread_nums)
logging_format = get_logger_logging_format()
thread_nums = get_thread_nums()

logger.add(sys.stderr, level="INFO", format=logging_format)
logger.add('spider/logs/other_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/other_logs/waringlog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/other_logs/errorlog_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')

task_queue_dict = {
    "doctor": queue.Queue(),
    "hospital": queue.Queue(),
}

def task(task_name, e_id):
    logger.info("task任务, 队列为:%s, id为:%s" % (task_name, str(e_id)))
    if task_name == "doctor":
        crawl_doctor_price(e_id)
        crawl_doctor_service_info(e_id)
        crawl_doctor_reward(e_id)
        crawl_doctor_comment_label(e_id)
        # crawl_illness_question(e_id)
    if task_name == "hospital":
        crawl_hospital_real_time_inquiry(e_id)


def action(done_list, task_queue, thread_order):
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
                    task(k, got_id)
                except Exception as e:
                    logger.exception(e)


def init_queue():
    with open("doctor_id.json", "r") as f:
        result = json.load(f)
        for item in result:
            task_queue_dict["doctor"].put(item)
        logger.info("医生信息抓取任务初始化成功")
    with open("hospital_id.json", "r") as f:
        result = json.load(f)
        for item in result:
            task_queue_dict["hospital"].put(item)
        logger.info("医院信息抓取任务初始化成功")

all_done = False
exited = False

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


def saver():
    while not all_done and not exited:
        for i in range(2 * 3):
            time.sleep(30)
            if all_done or exited:
                break
        do_save()


def do_save():
    save_dict = {}
    for k, v in task_queue_dict.items():
        save_dict[k] = list(v.queue)
    with open("queue_save.json", "w") as f:
        json.dump(save_dict, f)
    logger.info("queue保存成功")


def sig_handler(sig, frame):
    global exited
    exited = True
    logger.info('收到信号 signal %d, exited=%d' % (sig, exited))


def main():
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    pool = ThreadPoolExecutor(max_workers=thread_nums)
    done_list = [False for _ in range(thread_nums)]
    init_queue()
    for i in range(thread_nums):
        pool.submit(action, done_list, task_queue_dict, i)
    saver_thread = threading.Thread(target=saver)
    saver_thread.start()
    while not all_done and not exited:
        time.sleep(30)
    pool.shutdown(wait=True)
    saver_thread.join()
    do_save()
    logger.info("exit")


if __name__ == '__main__':
    main()
