import time
from .basic import Base
from .tables import *
from .tables import illness_info


class DoctorBaseInfo(Base):
    __table__ = doctor_base_info

class DoctorImg(Base):
    __table__ = doctor_img

class DoctorAuthInfo(Base):
    __table__ = doctor_auth_info

class DoctorServiceInfo(Base):
    __table__ = doctor_tag

class DoctorPrice(Base):
    __table__ = doctor_price

class DoctorDescription(Base):
    __table__ = doctor_description

class DoctorCommentLabel(Base):
    __table__ = doctor_comment_label

class IllnessInfo(Base):
    __table__ = illness_info

class DoctorReward(Base):
    __table__ = doctor_reward

class Hospital(Base):
    __table__ = hospital

class HospitalClinicEnterDoctor(Base):
    __table__ = hospital_clinic_enter_doctor

class HospitalRealTimeInquiry(Base):
    __table__ = hospital_real_time_inquiry

class HospitalClinicBaseInfo(Base):
    __table__ = hospital_clinic_base_info

class HospitalRank(Base):
    __table__ = hospital_rank

class hospital_clinic_rank(Base):
    __table__ = hospital_clinic_rank

class DoctorHospitalRelationship(Base):
    __table__ = doctor_hospital_relationship

class FirstClinic(Base):
    __table__ = first_clinic

class SecondClinic(Base):
    __table__ = second_clinic



