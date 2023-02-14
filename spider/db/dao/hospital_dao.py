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

class HospitalOper(CommonOper):
    @classmethod
    def get_hospital_base_info_by_hospital_id(cls, hospital_id):
        return db_session.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()

    @classmethod
    def update_hospital_by_hospital_id(cls, data):
        hospital = db_session.query(Hospital).filter(Hospital.hospital_id == data.hospital_id).first()
        hospital.hospital_name = data.hospital_name
        db_session.flush()
        db_session.commit()

    @classmethod
    def add_hospital_base_with_query(cls, datas):
        for data in datas:
            if not cls.get_hospital_base_info_by_hospital_id(data.hospital_id):
                cls.add_one(data)
            else:
                cls.update_hospital_by_hospital_id(data)

class HospitalClinicEnterDoctorOper(CommonOper):
    @classmethod
    def get_hosital_clinic_enter_doctor_by_hospital_id(cls, hospital_id):
        return db_session.query(HospitalClinicEnterDoctor).filter(HospitalClinicEnterDoctor.hospital_id == hospital_id).first()

class HospitalRealTimeInquiryOper(CommonOper):
    @classmethod
    def get_hospital_realtime_inquiry_by_hospital_id(cls, hospital_id):
        return db_session.query(HospitalRealTimeInquiry).filter(HospitalRealTimeInquiry.hospital_id == hospital_id).first()

class HospitalClinicBaseInfoOper(CommonOper):
    @classmethod
    def get_hospital_clinic_base_info_by_clinic_id(cls, clinic_id):
        return db_session.query(HospitalClinicBaseInfo).filter(HospitalClinicBaseInfo.hospital_clinic_id == clinic_id).first()

class HospitalRankOper(CommonOper):
    @classmethod
    def get_hospital_rank_by_hospital_id(cls, hospital_id):
        return db_session.query(HospitalRank).filter(HospitalRank.hospital_id == hospital_id).first()


class HospitalClinicRankOper(CommonOper):
    @classmethod
    def get_hospital_clinic_rank_by_hospital_id(cls, hospital_id):
        return db_session.query(HospitalClinicRank).filter(HospitalClinicRank.hospital_id == hospital_id).first()
