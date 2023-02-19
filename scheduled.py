import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from multiprocessing import Process
from spider.task.crawl_task import *
from spider.util.log_util import create_crawl_logger
logger = create_crawl_logger()

def doctor_high_frenquency_process():
    crawl_process = Process(target=crawl_doctor_high_fruency_info_task)
    crawl_process.start()

def doctor_status_task_process():
    crawl_process = Process(target=crawl_doctor_status_task)
    crawl_process.start()

def doctor_anti_status_task_process():
    crawl_process = Process(target=crawl_doctor_anti_status_task)
    crawl_process.start()

def hospital_high_frequency_process():
    crawl_process = Process(target=crawl_realtime_inquiry_task)
    crawl_process.start()

def recommend_doctor_process():
    crawl_process = Process(target=crawl_recommend_doctor_task)
    crawl_process.start()

if __name__ == '__main__':
    sche = BlockingScheduler(timezone='Asia/Shanghai')
    sche.add_job(hospital_high_frequency_process, CronTrigger.from_crontab('3 */4 * * *', timezone='Asia/Shanghai'))
    sche.add_job(doctor_high_frenquency_process, CronTrigger.from_crontab('11 1 * * *', timezone='Asia/Shanghai'))
    sche.add_job(recommend_doctor_process, CronTrigger.from_crontab('35 6 * * *', timezone='Asia/Shanghai'))
    sche.add_job(doctor_anti_status_task_process, CronTrigger.from_crontab('1 12 * * *', timezone='Asia/Shanghai'))
    sche.add_job(doctor_status_task_process, CronTrigger.from_crontab('5 21 * * *', timezone='Asia/Shanghai'))
    sche.start()
