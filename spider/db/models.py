from .basic import Base
from .tables import *
from .tables import illness_info


class DoctorBaseInfo(Base):
    __table__ = doctor_base_info
    __table_args__ = ({'comment': '医生基本信息'})

class DoctorImg(Base):
    __table__ = doctor_img
    __table_args__ = ({'comment': '医生头像信息'})

class DoctorAuthInfo(Base):
    __table__ = doctor_auth_info
    __table_args__ = ({'comment': '医生认证信息'})

class DoctorTag(Base):
    __table__ = doctor_tag
    __table_args__ = ({'comment': '医生基本标签信息'})

class DoctorServiceInfo(Base):
    __table__ = doctor_service_info
    __table_args__ = ({'comment': '医生基本服务信息'})

class DoctorPrice(Base):
    __table__ = doctor_price
    __table_args__ = ({'comment': '医生问诊价格信息'})

class DoctorDescription(Base):
    __table__ = doctor_description
    __table_args__ = ({'comment': '医生个人介绍信息'})

class DoctorCommentLabel(Base):
    __table__ = doctor_comment_label
    __table_args__ = ({'comment': '医生患者评价标签信息'})

class IllnessInfo(Base):
    __table__ = illness_info
    __table_args__ = ({'comment': '医生好评问题信息'})

class DoctorReward(Base):
    __table__ = doctor_reward
    __table_args__ = ({'comment': '医生心意墙信息'})

class Hospital(Base):
    __table__ = hospital
    __table_args__ = ({'comment': '医院基本信息'})

class HospitalClinicEnterDoctor(Base):
    __table__ = hospital_clinic_enter_doctor
    __table_args__ = ({'comment': '医院医生入驻信息'})

class HospitalRealTimeInquiry(Base):
    __table__ = hospital_real_time_inquiry
    __table_args__ = ({'comment': '医院科室基本信息'})

class HospitalClinicBaseInfo(Base):
    __table__ = hospital_clinic_base_info
    __table_args__ = ({'comment': '医院科室基本信息'})

class HospitalRank(Base):
    __table__ = hospital_rank
    __table_args__ = ({'comment': '医院综合排名信息'})

class HospitalClinicRank(Base):
    __table__ = hospital_clinic_rank
    __table_args__ = ({'comment': '医院各科室排名信息'})

class DoctorHospitalRelationship(Base):
    __table__ = doctor_hospital_relationship
    __table_args__ = ({'comment': '医院医生多对多关系信息'})

class FirstClinic(Base):
    __table__ = first_clinic
    __table_args__ = ({'comment': '一级科室信息'})

class SecondClinic(Base):
    __table__ = second_clinic
    __table_args__ = ({'comment': '二级科室信息'})



