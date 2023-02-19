import threading
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError

from spider.db.basic import db_session
from spider.db.models import *
from spider.decorators.storage_decorator import db_commit_decorator

local = threading.local()

class CommonOper:
    @classmethod
    @db_commit_decorator
    def add_one(cls, data):
        db_session.add(data)
        db_session.flush()
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def add_all(cls, datas):
        try:
            db_session.add_all(datas)
            db_session.flush()
            db_session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add_one(data)


class DoctorBaseInfoOper(CommonOper):
    @classmethod
    def get_doctor_base_info_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorBaseInfo).filter(DoctorBaseInfo.doctor_id == doctor_id).first()

    @classmethod
    def get_doctor_name_by_doctor_id(cls, doctor_id):
        doctor = db_session.query(DoctorBaseInfo).filter(DoctorBaseInfo.doctor_id == doctor_id).first()
        return doctor.doctor_name

    @classmethod
    @db_commit_decorator
    def update_doctor_base_by_doctor_id(cls, data):
        doctor = db_session.query(DoctorBaseInfo).filter(DoctorBaseInfo.doctor_id == data.doctor_id).first()
        doctor.doctor_name = data.doctor_name
        db_session.flush()
        db_session.commit()

    @classmethod
    def add_doctor_base_with_query(cls, datas):
        for data in datas:
            if not cls.get_doctor_base_info_by_doctor_id(data.doctor_id):
                cls.add_one(data)
            else:
                cls.update_doctor_base_by_doctor_id(data)



class DoctorImgOper(CommonOper):
    @classmethod
    def get_doctor_img_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorImg).filter(DoctorImg.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_doctor_img_by_doctor_id(cls, data):
        doctor = db_session.query(DoctorImg).filter(DoctorImg.doctor_id == data.doctor_id).first()
        doctor.doctor_img_remote_path = data.doctor_img_remote_path
        db_session.flush()
        db_session.commit()

    @classmethod
    def add_doctor_img_with_query(cls, datas):
        for data in datas:
            if not cls.get_doctor_img_by_doctor_id(data.doctor_id):
                cls.add_one(data)
            else:
                pass


class DoctorAuthInfoOper(CommonOper):
    @classmethod
    def get_doctor_auth_info_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorAuthInfo).filter(DoctorAuthInfo.doctor_id == doctor_id).all()

    @classmethod
    @db_commit_decorator
    def update_auth_info_by_doctor_id(cls, data):
        auth = db_session.query(DoctorAuthInfo).filter(DoctorAuthInfo.doctor_id == data.doctor_id).first()
        auth.doctor_auth_status = data.doctor_auth_status
        auth.doctor_auth_hospital_id = data.doctor_auth_hospital_id
        auth.doctor_auth_clinic_id = data.doctor_auth_clinic_id
        auth.doctor_auth_grade = data.doctor_auth_grade
        auth.doctor_auth_time = data.doctor_auth_time
        db_session.flush()
        db_session.commit()


class DoctorTagOper(CommonOper):
    @classmethod
    def get_doctor_tag_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorTag).filter(DoctorTag.doctor_id == doctor_id).all()

    @classmethod
    @db_commit_decorator
    def update_tag_by_doctor_id(cls, data):
        tag = db_session.query(DoctorTag).filter(DoctorTag.doctor_id == data.doctor_id).first()
        tag.tag_content = data.tag_content
        db_session.flush()
        db_session.commit()
    

class DoctorServiceInfoOper(CommonOper):
    @classmethod
    def get_doctor_service_info_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorServiceInfo).filter(DoctorServiceInfo.doctor_id == doctor_id).all()

    @classmethod
    @db_commit_decorator
    def update_service_info_by_doctor_id(cls, data):
        service = db_session.query(DoctorServiceInfo).filter(DoctorServiceInfo.doctor_id == data.doctor_id).first()
        service.doctor_serve_nums = data.doctor_serve_nums
        service.doctor_serve_favorable_rate = data.doctor_serve_favorable_rate
        service.doctor_serve_peer_recognization = data.doctor_serve_peer_recognization
        service.doctor_serve_patient_praise_num = data.doctor_serve_patient_praise_num
        service.doctor_serve_followers = data.doctor_serve_followers
        db_session.flush()
        db_session.commit()

class DoctorPriceOper(CommonOper):
    @classmethod
    def get_doctor_price_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorPrice).filter(DoctorPrice.doctor_id == doctor_id).first()

class DoctorDescriptionOper(CommonOper):
    @classmethod
    def get_doctor_description_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorDescription).filter(DoctorDescription.doctor_id == doctor_id).all()

    @classmethod
    @db_commit_decorator
    def update_description_info_by_doctor_id(cls, data):
        description = db_session.query(DoctorDescription).filter(DoctorDescription.doctor_id == data.doctor_id).first()
        description.doctor_description_edu_background = data.doctor_description_edu_background
        description.doctor_description_major = data.doctor_description_major
        description.doctor_description_description = data.doctor_description_description
        description.doctor_description_hospital_location = data.doctor_description_hospital_location
        db_session.flush()
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def update_by_mobile_page(cls, data):
        description = db_session.query(DoctorDescription).filter(DoctorDescription.doctor_id == data.doctor_id).first()
        description.doctor_description_edu_background = data.doctor_description_edu_background
        description.doctor_description_major = data.doctor_description_major
        db_session.flush()
        db_session.commit()


class DoctorCommentLabelOper(CommonOper):
    @classmethod
    def get_doctor_comment_label_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorCommentLabel).filter(DoctorCommentLabel.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_comment_label_by_doctor_id(cls, data):
        label = db_session.query(DoctorCommentLabel).filter(DoctorCommentLabel.doctor_id == data.doctor_id).first()
        label.doctor_comment_attitude = data.doctor_comment_attitude
        label.doctor_comment_explanation = data.doctor_comment_explanation
        label.doctor_comment_reply = data.doctor_comment_reply
        label.doctor_comment_suggestion = data.doctor_comment_suggestion
        db_session.flush()
        db_session.commit()

class DoctorRewardOper(CommonOper):
    @classmethod
    def get_doctor_reward_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorReward).filter(DoctorReward.doctor_id == doctor_id).first()


class DoctorIllnessOper(CommonOper):
    @classmethod
    def get_doctor_illness_by_doctor_id(cls, doctor_id):
        return db_session.query(IllnessInfo).filter(IllnessInfo.doctor_id == doctor_id).all()

    @classmethod
    def get_doctor_illness_by_question_id(cls, question_id):
        return db_session.query(IllnessInfo).filter(IllnessInfo.illness_question_id == question_id).all()

    @classmethod
    def get_doctor_id_by_question_id(cls, question_id):
        illness = db_session.query(IllnessInfo).filter(IllnessInfo.illness_question_id == question_id).first()
        return illness.doctor_id

    @classmethod
    @db_commit_decorator
    def update_illness_by_question_id(cls, data):
        illness = db_session.query(IllnessInfo).filter(IllnessInfo.illness_question_id == data.illness_question_id).first()
        illness.clinic_id = data.clinic_id
        illness.illness_detail_html = data.illness_detail_html
        db_session.flush()
        db_session.commit()

    @classmethod
    def add_illness_with_datas_query(cls, datas):
        for data in datas:
            if not cls.get_doctor_illness_by_question_id(data.illness_question_id):
                cls.add_one(data)
            else:
                cls.update_illness_by_question_id(data)

class DoctorRecommendOper(CommonOper):

    @classmethod
    def get_doctor_recommend_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorRecommend).filter(DoctorRecommend.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_doctor_recommend_by_doctor_id(cls, data):
        doctor = db_session.query(DoctorRecommend).filter(DoctorRecommend.doctor_id == data.doctor_id).first()
        doctor.recommend_doctor_is_inquiry = data.recommend_doctor_is_inquiry
        db_session.flush()
        db_session.commit()

    @classmethod
    def add_doctor_recommend_with_query(cls, datas):
        for data in datas:
            if not cls.get_doctor_recommend_by_doctor_id(data.doctor_id):
                cls.add_one(data)
            else:
                pass

class DoctorStatusOper(CommonOper):
    @classmethod
    def get_doctor_status_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorStatus).filter(DoctorStatus.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_status_by_data(cls, data):
        ds = cls.get_doctor_status_by_doctor_id(data.doctor_id)
        ds.is_page_404 = data.is_page_404
        ds.is_anti_crawl = data.is_anti_crawl
        ds.is_price_exist = data.is_price_exist
        ds.is_comment_label_exist = data.is_comment_label_exist
        ds.is_service_info_exist = data.is_service_info_exist
        ds.is_illness_question_exist = data.is_illness_question_exist
        ds.is_reward_exist = data.is_reward_exist
        db_session.flush()
        db_session.commit()

    @classmethod
    @db_commit_decorator
    def update_status_by_price(cls, data):
        ds = cls.get_doctor_status_by_doctor_id(data.doctor_id)
        ds.is_page_404 = data.is_page_404
        ds.is_anti_crawl = data.is_anti_crawl
        ds.is_price_exist = data.is_price_exist
        db_session.flush()
        db_session.commit()

class DoctorHighFrequencyStatusOper(CommonOper):
    @classmethod
    def get_status_by_doc_id(cls, doctor_id):
        return db_session.query(DoctorHighFrequencyStatus).filter(DoctorHighFrequencyStatus.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_staus_with_data(cls, data):
        dhfs = cls.get_status_by_doc_id(data.doctor_id)
        if not dhfs:
            cls.add_one(data)
        else:
            dhfs.is_price_crawl = data.is_price_crawl
            dhfs.is_service_info_crawl = data.is_service_info_crawl
            dhfs.is_comment_label_crawl = data.is_comment_label_crawl
            db_session.flush()
            db_session.commit()


class DoctorMidFrequencyStatusOper(CommonOper):
    @classmethod
    def get_status_by_doc_id(cls, doctor_id):
        return db_session.query(DoctorMidFrequencyStatus).filter(DoctorMidFrequencyStatus.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_staus_with_data(cls, data):
        dmfs = cls.get_status_by_doc_id(data.doctor_id)
        if not dmfs:
            cls.add_one(data)
        else:
            dmfs.is_reward_crawl = data.is_reward_crawl
            db_session.flush()
            db_session.commit()

class DoctorLowFrequencyStatusOper(CommonOper):
    @classmethod
    def get_status_by_doc_id(cls, doctor_id):
        return db_session.query(DoctorLowFrequencyStatus).filter(DoctorLowFrequencyStatus.doctor_id == doctor_id).first()

    @classmethod
    @db_commit_decorator
    def update_staus_with_data(cls, data):
        dlfs = cls.get_status_by_doc_id(data.doctor_id)
        if not dlfs:
            cls.add_one(data)
        else:
            dlfs.is_auth_crawl = data.is_auth_crawl
            dlfs.is_description_crawl = data.is_description_crawl
            dlfs.is_tag_crawl = data.is_tag_crawl
            db_session.flush()
            db_session.commit()






