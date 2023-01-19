
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError

from spider.db.basic import db_session
from spider.db.models import *


class CommonOper:
    @classmethod
    def add_one(cls, data):
        db_session.add(data)
        db_session.commit()

    @classmethod
    def add_all(cls, datas):
        try:
            db_session.add_all(datas)
            db_session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            for data in datas:
                cls.add_one(data)


class DoctorBaseInfoOper(CommonOper):
    @classmethod
    def get_doctor_base_info_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorBaseInfo).filter(DoctorBaseInfo.doctor_id == doctor_id).first()


class DoctorImgOper(CommonOper):
    @classmethod
    def get_doctor_img_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorImg).filter(DoctorImg.doctor_id == doctor_id).first()


class DoctorAuthInfoOper(CommonOper):
    @classmethod
    def get_doctor_auth_info_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorAuthInfo).filter(DoctorAuthInfo.doctor_id == doctor_id).first()

class DoctorTagOper(CommonOper):
    @classmethod
    def get_doctor_tag_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorTag).filter(DoctorTag.doctor_id == doctor_id).first()

class DoctorServiceInfoOper(CommonOper):
    @classmethod
    def get_doctor_service_info_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorServiceInfo).filter(DoctorServiceInfo.doctor_id == doctor_id).first()

class DoctorPriceOper(CommonOper):
    @classmethod
    def get_doctor_price_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorPrice).filter(DoctorPrice.doctor_id == doctor_id).first()

class DoctorDescriptionOper(CommonOper):
    @classmethod
    def get_doctor_description_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorDescription).filter(DoctorDescription.doctor_id == doctor_id).first()

class DoctorCommentLabelOper(CommonOper):
    @classmethod
    def get_doctor_comment_label_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorCommentLabel).filter(DoctorCommentLabel.doctor_id == doctor_id).first()

class DoctorRewardOper(CommonOper):
    @classmethod
    def get_doctor_reward_by_doctor_id(cls, doctor_id):
        return db_session.query(DoctorReward).filter(DoctorReward.doctor_id == doctor_id).first()

class DoctorIllnessOper(CommonOper):
    @classmethod
    def get_doctor_illness_by_doctor_id(cls, doctor_id):
        return db_session.query(IllnessInfo).filter(IllnessInfo.doctor_id == doctor_id).first()