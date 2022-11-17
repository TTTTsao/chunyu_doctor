from sqlalchemy import (
    Table, Column, INTEGER, String, Text, TIMESTAMP, DateTime, func, SMALLINT, JSON, DECIMAL)

from .basic import metadata

# raw_doctor_base_info
doctor_base_info = Table('raw_doctor_base_info', metadata,
                         Column("id", INTEGER, primary_key=True, autoincrement=True),
                         Column("doctor_id", String(50), unique=True),
                         Column("doctor_name", String(50)),
                         Column("created_at", DateTime),
                         Column("updated_at", TIMESTAMP),
                         )

# raw_doctor_img
doctor_img = Table('raw_doctor_img', metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                   Column("doctor_id", String(50), unique=True),
                   Column("doctor_img_local_path", String(511)),
                   Column("doctor_img_remote_path", String(511)),
                   Column("created_at", DateTime),
                   Column("updated_at", TIMESTAMP),
                   )

# raw_doctor_auth_info
doctor_auth_info = Table('raw_doctor_auth_info', metadata,
                         Column("id", INTEGER, primary_key=True, autoincrement=True),
                         Column("doctor_id", String(50), unique=True),
                         Column("doctor_auth_status", SMALLINT),
                         Column("doctor_auth_hospital_id", String(50)),
                         Column("doctor_auth_clinic_id", String(50)),
                         Column("doctor_auth_grade", String(90)),
                         Column("doctor_auth_time", DateTime),
                         Column("created_at", DateTime),
                         Column("updated_at", TIMESTAMP),
                         )

# raw_doctor_tag
doctor_tag = Table('raw_doctor_tag', metadata,
                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                   Column("doctor_id", String(50), unique=True),
                   Column("tag_content", JSON),
                   Column("created_at", DateTime),
                   Column("updated_at", TIMESTAMP),
                   )

# raw_doctor_service_info
doctor_service_info = Table("raw_doctor_service_info", metadata,
                            Column("id", INTEGER, primary_key=True, autoincrement=True),
                            Column("doctor_id", String(50), unique=True),
                            Column("doctor_serve_nums", INTEGER),
                            Column("doctor_serve_favorable_rate", DECIMAL),
                            Column("doctor_serve_peer_recognization", DECIMAL),
                            Column("doctor_serve_patient_praise_num", INTEGER),
                            Column("doctor_serve_followers", INTEGER),
                            Column("created_at", DateTime),
                            Column("updated_at", TIMESTAMP),
                            )

# raw_doctor_price
doctor_price = Table('raw_doctor_price', metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True),
                     Column("doctor_id", String(50), unique=True),
                     Column("doctor_price", DECIMAL),
                     Column("doctor_price_discount", DECIMAL),
                     Column("doctor_price_type", String(32)),
                     Column("created_at", DateTime),
                     Column("updated_at", TIMESTAMP),
                     )

# raw_doctor_description
doctor_description = Table('raw_doctor_description', metadata,
                           Column("id", INTEGER, primary_key=True, autoincrement=True),
                           Column("doctor_id", String(50), unique=True),
                           Column("doctor_description_edu_background", Text),
                           Column("doctor_description_major", Text),
                           Column("doctor_description_description", Text),
                           Column("doctor_description_hospital_location", Text),
                           Column("created_at", DateTime),
                           Column("updated_at", TIMESTAMP),
                           )

# raw_doctor_comment_label
doctor_comment_label = Table('raw_doctor_comment_label', metadata,
                             Column("id", INTEGER, primary_key=True, autoincrement=True),
                             Column("doctor_id", String(50), unique=True),
                             Column("doctor_comment_attitude", INTEGER),
                             Column("doctor_comment_explanation", INTEGER),
                             Column("doctor_comment_reply", INTEGER),
                             Column("doctor_comment_suggestion", INTEGER),
                             Column("created_at", DateTime),
                             Column("updated_at", TIMESTAMP),
                             )

# raw_html_illness
illness_info = Table('raw_html_illness', metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True),
                     Column("doctor_id", String(50), unique=True),
                     Column("illness_question_id", String(255)),
                     Column("clinic_id", String(50)),
                     Column("illness_type", String(32)),
                     Column("illness_time", DateTime),
                     Column("illness_title", String(255)),
                     Column("illness_detail_html", Text),
                     Column("created_at", DateTime),
                     Column("updated_at", TIMESTAMP),
                     )

# raw_doctor_reward
doctor_reward = Table('raw_doctor_reward', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True),
                      Column("doctor_id", String(50), unique=True),
                      Column("doctor_reward_datetime", DateTime),
                      Column("doctor_reward_amount", DECIMAL),
                      Column("doctor_reward_content", String(255)),
                      Column("created_at", DateTime),
                      Column("updated_at", TIMESTAMP),
                      )

# raw_hospital
hospital = Table('raw_hospital', metadata,
                 Column("id", INTEGER, primary_key=True, autoincrement=True),
                 Column("hospital_id", String(50), unique=True),
                 Column("hospital_name", String(50)),
                 Column("hospital_area", String(20)),
                 Column("hospital_province", String(20)),
                 Column("hospital_city", String(90)),
                 Column("hospital_profile", Text),
                 Column("hospital_tag", JSON),
                 Column("created_at", DateTime),
                 Column("updated_at", TIMESTAMP),
                 )

# raw_hospital_clinic_enter_doctor
hospital_clinic_enter_doctor = Table('raw_hospital_clinic_enter_doctor', metadata,
                                     Column("id", INTEGER, primary_key=True, autoincrement=True),
                                     Column("hospital_id", String(50), unique=True),
                                     Column("hospital_clinic_id", String(50)),
                                     Column("hospital_clinic_amount", INTEGER),
                                     Column("created_at", DateTime),
                                     Column("updated_at", TIMESTAMP),
                                     )

# raw_hospital_real_time_inquiry
hospital_real_time_inquiry = Table('raw_hospital_real_time_inquiry', metadata,
                                   Column("id", INTEGER, primary_key=True, autoincrement=True),
                                   Column("hospital_id", String(50), unique=True),
                                   Column("real_time_inquiry_doctor_num", INTEGER),
                                   Column("created_at", DateTime),
                                   Column("updated_at", TIMESTAMP),
                                   )

# raw_hospital_clinic_base_info
hospital_clinic_base_info = Table('raw_hospital_clinic_base_info', metadata,
                                  Column("id", INTEGER, primary_key=True, autoincrement=True),
                                  Column("hospital_clinic_id", String(50)),
                                  Column("hospital_clinic_name", String(255)),
                                  Column("hospital_clinic_profile", Text),
                                  Column("created_at", DateTime),
                                  Column("updated_at", TIMESTAMP),
                                  )

# raw_hospital_rank
hospital_rank = Table('raw_hospital_rank', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True),
                      Column("hospital_id", String(50), unique=True),
                      Column("hospital_rank_area", String(255)),
                      Column("hospital_rank_province", String(255)),
                      Column("hospital_rank_city", String(255)),
                      Column("hospital_rank_first_clinic", String(90)),
                      Column("hospital_rank_second_clinic", String(90)),
                      Column("hospital_hospital_rank", INTEGER),
                      Column("hospital_rank_register_way", Text),
                      Column("created_at", DateTime),
                      Column("updated_at", TIMESTAMP),
                      )

# raw_hospital_clinic_rank
hospital_clinic_rank = Table('raw_hospital_clinic_rank', metadata,
                             Column("id", INTEGER, primary_key=True, autoincrement=True),
                             Column("hospital_id", String(50), unique=True),
                             Column('rank_name', String(90)),
                             Column('rank_level', INTEGER),
                             Column("created_at", DateTime),
                             Column("updated_at", TIMESTAMP),
                             )

# raw_first_clinic
first_clinic = Table('raw_first_clinic', metadata,
                     Column("id", INTEGER, primary_key=True, autoincrement=True),
                     Column("first_clinic_id", String(255)),
                     Column("first_clinic_name", String(90)),
                     Column("created_at", DateTime),
                     Column("updated_at", TIMESTAMP),
                     )

# raw_second_clinic
second_clinic = Table('raw_second_clinic', metadata,
                      Column("id", INTEGER, primary_key=True, autoincrement=True),
                      Column("first_clinic_id", String(255)),
                      Column("second_clinic_id", String(255)),
                      Column("second_clinic_name", String(90)),
                      Column("created_at", DateTime),
                      Column("updated_at", TIMESTAMP),
                      )