import sys
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from spider.config.conf import get_logger_logging_format
from spider.task.tasks_daily.doctor_daily_crawl import doctor_daily_process
from spider.task.tasks_hourly.real_time_inquiry_crawl import real_time_inquiry_process
from spider.task.tasks_monthly.doctor_monthly_crawl import doctor_monthly_process
from spider.task.tasks_seminually.doctor_seminually_crawl import doctor_seminually_process
logging_format = get_logger_logging_format()
logger.remove()
logger.add(sys.stderr, level="INFO", format=logging_format)
logger.add('spider/logs/other_logs/runlog_{time}.log', level="INFO", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/other_logs/warninglog_{time}.log', level="WARNING", format=logging_format, rotation="20 MB", encoding='utf-8')
logger.add('spider/logs/other_logs/error_{time}.log', level="ERROR", format=logging_format, rotation="20 MB", encoding='utf-8')

def hourly():
    real_time_inquiry_process()

def daily():
    doctor_daily_process()

def weekly():
    pass

def monthly():
    doctor_monthly_process()

def seminually():
    # doctor: auth_info, img_info, tag, description
    doctor_seminually_process()
    # hospital/clinic rank
    pass

def yearly():
    # doctor: base_info,
    # hospital: base_info, clinic_info,
    pass


if __name__ == '__main__':
    sche = BlockingScheduler(timezone='Asia/Shanghai')
    sche.add_job(hourly, CronTrigger.from_crontab('0 */2 * * *', timezone='Asia/Shanghai'))
    sche.add_job(daily, CronTrigger.from_crontab('0 8 * * *', timezone='Asia/Shanghai'))
    # sche.add_job(weekly, CronTrigger.from_crontab('0 7 * * 1,4', timezone='Asia/Shanghai'))
    sche.add_job(monthly, CronTrigger.from_crontab('0 8 1 * *', timezone='Asia/Shanghai'))
    sche.add_job(seminually, CronTrigger.from_crontab('15 7 1 2,8 *', timezone='Asia/Shanghai'))
    sche.start()
