from spider.task.doctor.base_info import crawl_all_doctor_base_info
from spider.task.doctor.detail_info import crawl_all_doctor_detail_info
from spider.task.hospital.hospital_info import (crawl_all_hospital_base_info, crawl_all_hospital_clinic_base_info)

if __name__ == '__main__':
    # crawl_all_doctor_base_info()
    crawl_all_doctor_detail_info()
    # crawl_all_hospital_base_info()
    # crawl_all_hospital_clinic_base_info()