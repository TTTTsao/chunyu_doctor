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

class ClinicOper(CommonOper):
    @classmethod
    def get_clinic_name_by_clinic_id(cls, clinic_id):
        return db_session.query(Clinic).filter(Clinic.clinic_id == clinic_id).first()