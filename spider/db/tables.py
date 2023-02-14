import datetime

from sqlalchemy import (
    Table, Column, INTEGER, String, Text, TIMESTAMP, DateTime, func, SMALLINT, JSON, DECIMAL)

from .basic import metadata

# raw_doctor_base_info
doctor_base_info = Table('raw_doctor_base_info', metadata,
                         Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                         Column("doctor_id", String(50), comment="医生id"),
                         Column("doctor_name", String(50), comment="医生名字"),
                         Column("created_at", DateTime, default=datetime.datetime.now, comment="抓取时间"),
                         Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                         )

# raw_doctor_img
doctor_img = Table('raw_doctor_img', metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                   Column("doctor_id", String(50), comment="医生id"),
                   Column("doctor_img_local_path", String(511), comment="头像本地路径"),
                   Column("doctor_img_remote_path", String(511), comment="头像url"),
                   Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                   Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                   )

# raw_doctor_auth_info
doctor_auth_info = Table('raw_doctor_auth_info', metadata,
                         Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                         Column("doctor_id", String(50), comment="医生id"),
                         Column("doctor_auth_status", SMALLINT, comment="医生认证状态"),
                         Column("doctor_auth_hospital_id", String(50), comment="医生认证医院id"),
                         Column("doctor_auth_clinic_id", String(50), comment="医生认证科室id"),
                         Column("doctor_auth_grade", String(50), comment="医生认证职称"),
                         Column("doctor_auth_time", String(32), comment="医生认证时间"),
                         Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                         Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                         )

# raw_doctor_tag
doctor_tag = Table('raw_doctor_tag', metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                   Column("doctor_id", String(50), comment="医生id"),
                   Column("tag_content", JSON, comment="医生标签（JSON格式存储）"),
                   Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                   Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                   )

# raw_doctor_service_info
doctor_service_info = Table("raw_doctor_service_info", metadata,
                            Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                            Column("doctor_id", String(50), comment="医生id"),
                            Column("doctor_serve_nums", INTEGER, comment="服务人次"),
                            Column("doctor_serve_favorable_rate", DECIMAL, comment="好评率"),
                            Column("doctor_serve_peer_recognization", DECIMAL, comment="同行认可"),
                            Column("doctor_serve_patient_praise_num", INTEGER, comment="患者心意"),
                            Column("doctor_serve_followers", INTEGER, comment="关注人数"),
                            Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                            Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                            )

# raw_doctor_price
doctor_price = Table('raw_doctor_price', metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                     Column("doctor_id", String(50), comment="医生id"),
                     Column("doctor_price", DECIMAL, comment="医生问诊价格"),
                     Column("doctor_price_discount", DECIMAL, comment="医生问诊折扣"),
                     Column("doctor_price_type", String(32), comment="医生问诊类型"),
                     Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                     Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                     )

# raw_doctor_description
doctor_description = Table('raw_doctor_description', metadata,
                           Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                           Column("doctor_id", String(50), comment="医生id"),
                           Column("doctor_description_edu_background", Text, comment="医生医学教育背景"),
                           Column("doctor_description_major", Text, comment="医生专业擅长"),
                           Column("doctor_description_description", Text, comment="医生个人简介"),
                           Column("doctor_description_hospital_location", Text, comment="医生医院地点"),
                           Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                           Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                           )

# raw_doctor_comment_label
doctor_comment_label = Table('raw_doctor_comment_label', metadata,
                             Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                             Column("doctor_id", String(50), comment="医生id"),
                             Column("doctor_comment_attitude", INTEGER, comment="【态度非常好】数量"),
                             Column("doctor_comment_explanation", INTEGER, comment="【讲解很清楚】数量"),
                             Column("doctor_comment_reply", INTEGER, comment="【回复很及时】数量"),
                             Column("doctor_comment_suggestion", INTEGER, comment="【建议很有帮助】数量"),
                             Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                             Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                             )

# raw_html_illness
illness_info = Table('raw_html_illness', metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                     Column("doctor_id", String(50), comment="医生id"),
                     Column("illness_question_id", String(255), comment="问题id"),
                     Column("clinic_id", String(50), comment="科室id"),
                     Column("illness_type", String(32), comment="问题类型"),
                     Column("illness_time", DateTime, comment="提问时间"),
                     Column("illness_title", String(255), comment="提问题目"),
                     Column("illness_detail_html", Text, comment="提问问答详情html"),
                     Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                     Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                     )

# raw_doctor_reward
doctor_reward = Table('raw_doctor_reward', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                      Column("doctor_id", String(50), comment="医生id"),
                      Column("doctor_reward_datetime", DateTime, comment="打赏时间"),
                      Column("doctor_reward_amount", DECIMAL, comment="打赏金额"),
                      Column("doctor_reward_content", String(255), comment="打赏留言"),
                      Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                      Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                      )

# raw_hospital
hospital = Table('raw_hospital', metadata,
                 Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                 Column("hospital_id", String(50), comment="医院id"),
                 Column("hospital_name", String(50), comment="医院名字"),
                 Column("hospital_area", String(20), comment="医院所在地区"),
                 Column("hospital_province", String(20), comment="医院所在省份"),
                 Column("hospital_city", String(90), comment="医院所在城市"),
                 Column("hospital_profile", Text, comment="医院简介"),
                 Column("hospital_tag", JSON, comment="医院标签（JSON格式）"),
                 Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                 Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                 )

# raw_hospital_clinic_enter_doctor
hospital_clinic_enter_doctor = Table('raw_hospital_clinic_enter_doctor', metadata,
                                     Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                                     Column("hospital_id", String(50), comment="医院id"),
                                     Column("hospital_clinic_id", String(50), comment="医院科室id"),
                                     Column("hospital_clinic_amount", INTEGER, comment="入驻医生数量"),
                                     Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                                     Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                                     )

# raw_hospital_real_time_inquiry
hospital_real_time_inquiry = Table('raw_hospital_real_time_inquiry', metadata,
                                   Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                                   Column("hospital_id", String(50), comment="医院id"),
                                   Column("real_time_inquiry_doctor_num", INTEGER, comment="当前可咨询医生数量"),
                                   Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                                   Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                                   )

# raw_hospital_clinic_base_info
hospital_clinic_base_info = Table('raw_hospital_clinic_base_info', metadata,
                                  Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                                  Column("hospital_clinic_id", String(50), comment="医院科室id"),
                                  Column("hospital_clinic_name", String(255), comment="医院科室名称"),
                                  Column("hospital_clinic_profile", Text, comment="医院科室简介"),
                                  Column("created_at", DateTime, default=datetime.datetime.now, comment="抓取时间"),
                                  Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                                  )

# raw_hospital_rank
hospital_rank = Table('raw_hospital_rank', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                      Column("hospital_id", String(50), comment="医院id"),
                      Column("hospital_rank_area", String(255), comment="医院排名地区"),
                      Column("hospital_rank_province", String(255), comment="医院排名省份"),
                      Column("hospital_rank_city", String(255), comment="医院排名城市"),
                      Column("hospital_rank_clinic", String(90), comment="科室id"),
                      Column("hospital_hospital_rank", INTEGER, comment="医院排名名次"),
                      Column("hospital_rank_register_way", Text, comment="挂号方式"),
                      Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                      Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                      )

# raw_hospital_clinic_rank
hospital_clinic_rank = Table('raw_hospital_clinic_rank', metadata,
                             Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                             Column("hospital_id", String(50), comment="医院id"),
                             Column('rank_name', String(90), comment="排名单位名"),
                             Column('rank_level', INTEGER, comment="科室排名"),
                             Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                             Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                             )

# 【多对多表】医生医院表(废弃)
doctor_hospital_relationship = Table('doctor_hospital_relationship', metadata,
                        Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                        Column("doctor_id", String(50), comment="医生id"),
                        Column("hospital_id", String(50), comment="医院id"),
                        Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                        Column("updated_at", TIMESTAMP(True), nullable=False, comment="更新时间"),
                        )


# raw_recommend_doctor
recommend_doctor = Table('raw_recommend_doctor', metadata,
                         Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                         Column("doctor_id", String(50), comment="医生id"),
                         Column("hospital_id", String(50), comment="医院id"),
                         Column("clinic_id", String(50), comment="科室id"),
                         Column("recommend_doctor_is_inquiry", SMALLINT, comment="是否可咨询，0-不可咨询，1-可咨询"),
                         Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                         Column("updated_at", TIMESTAMP, comment="更新时间"),
                         )

# estimate_doctor_crawl_status
estimate_doctor_crawl_status = Table('estimate_doctor_crawl_status', metadata,
                                     Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                                     Column("doctor_id", String(50), comment="医生id"),
                                     Column("is_page_404", SMALLINT, comment="医生页面是否不存在，0-不存在，1-存在"),
                                     Column("is_anti_crawl", SMALLINT, comment="医生页面是否被反爬，0-被反爬，1-正常"),
                                     Column("is_price_exist", SMALLINT, comment="医生价格信息是否存在，0-不存在，1-存在"),
                                     Column("is_comment_label_exist", SMALLINT, comment="医生评价标签信息是否存在，0-不存在，1-存在"),
                                     Column("is_service_info_exist", SMALLINT, comment="医生服务信息是否存在，0-不存在，1-存在"),
                                     Column("is_illness_question_exist", SMALLINT, comment="医生问诊对话是否存在，0-不存在，1-存在"),
                                     Column("is_reward_exist", SMALLINT, comment="医生患者心意是否存在，0-不存在，1-存在"),
                                     Column("created_at", DateTime, default=datetime.datetime.now,  comment="抓取时间"),
                                     Column("updated_at", TIMESTAMP, comment="更新时间"),
                                     )

# estimate_doctor_high_frequency_info_status
estimate_doctor_high_frequency_info_status = Table('estimate_doctor_high_frequency_info_status', metadata,
                                                   Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                                                   Column("doctor_id", String(50), comment="医生id"),
                                                   Column("is_price_crawl", SMALLINT, comment="医生价格是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                   Column("is_comment_label_crawl", SMALLINT, comment="医生评价标签信息是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                   Column("is_service_info_crawl", SMALLINT, comment="医生服务信息是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                   Column("created_at", DateTime, default=datetime.datetime.now,comment="抓取时间"),
                                                   Column("updated_at", TIMESTAMP, comment="更新时间"),
                                                   )

# estimate_doctor_mid_frequency_info_status
estimate_doctor_mid_frequency_info_status = Table('estimate_doctor_mid_frequency_info_status', metadata,
                                                  Column("id", INTEGER, primary_key=True, autoincrement=True,comment="自增id"),
                                                  Column("doctor_id", String(50), comment="医生id"),
                                                  Column("is_reward_crawl", SMALLINT, comment="医生患者是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                  Column("created_at", DateTime, default=datetime.datetime.now,comment="抓取时间"),
                                                  Column("updated_at", TIMESTAMP, comment="更新时间"),
                                                  )

# estimate_doctor_low_frequency_info_status
estimate_doctor_low_frequency_info_status = Table('estimate_doctor_low_frequency_info_status', metadata,
                                                  Column("id", INTEGER, primary_key=True, autoincrement=True,comment="自增id"),
                                                  Column("doctor_id", String(50), comment="医生id"),
                                                  Column("is_auth_crawl", SMALLINT,comment="医生认证信息是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                  Column("is_description_crawl", SMALLINT,comment="医生简介信息是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                  Column("is_tag_crawl", SMALLINT,comment="医生标签信息是否抓取，0-未抓取，1-抓取，2-不需抓取"),
                                                  Column("created_at", DateTime, default=datetime.datetime.now,comment="抓取时间"),
                                                  Column("updated_at", TIMESTAMP, comment="更新时间"),
                                                  )

# raw_clinic
raw_clinic = Table("raw_clinic", metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True, comment="自增id"),
                   Column("clinic_id", String(255), comment="科室id"),
                   Column("clinic_name", String(90), comment="科室名"),
                   Column("created_at", DateTime, default=datetime.datetime.now, comment="抓取时间"),
                   Column("updated_at", TIMESTAMP, comment="更新时间"),
                   )



__all__ = ['doctor_base_info', 'doctor_img', 'doctor_auth_info', 'doctor_tag', 'doctor_service_info', 'doctor_price', 'doctor_description',
           'doctor_comment_label', 'doctor_reward', 'hospital', 'hospital_clinic_enter_doctor', 'hospital_real_time_inquiry',
           'hospital_clinic_base_info', 'hospital_rank', 'hospital_clinic_rank', 'doctor_hospital_relationship', 'recommend_doctor',
           'estimate_doctor_crawl_status', 'estimate_doctor_high_frequency_info_status',
           'estimate_doctor_mid_frequency_info_status', 'estimate_doctor_low_frequency_info_status', 'raw_clinic']