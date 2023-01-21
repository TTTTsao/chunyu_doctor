from spider.db.models import DoctorImg
from spider.util.reg.reg_doctor import get_reg_doctor_id
from spider.decorators.parse_decorator import parse_decorator

from lxml import etree

@parse_decorator(False)
def get_active_doctor_img(html):
    '''
    get active doctor img info data
    从【根据科室找医生】获取活跃的医生头像信息
    :param html:
    :return:
    '''
    if not html:
        return False

    doctor_img_datas = []
    xpath = etree.HTML(html)
    doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_img_url_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[1]/a/img/@src")

    for i in range(len(doctor_id_list)):
        doctor_img = DoctorImg()
        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_img.doctor_id = doctor_id
        doctor_img_url = str(doctor_img_url_list[i])
        doctor_img.doctor_img_remote_path = doctor_img_url
        doctor_img_datas.append(doctor_img)

    return doctor_img_datas

@parse_decorator
def get_doctor_img_from_clinic(html):
    '''
    get doctor img info from clinic page
    从科室详情页获取医生头像信息
    :param html:
    :return:
    '''
    if not html:
        return False
    xpath = etree.HTML(html)
    try:
        doctor_id_list = xpath.xpath("//div[@class='avatar-wrap']/a/@href")
        doctor_img_url_list = xpath.xpath("//div[@class='avatar-wrap']/a/img/@src")
    except Exception:
        return False

    # 判断页面有无医生
    if len(doctor_id_list) == 0: return

    doctor_img_datas = []
    for i in range(len(doctor_id_list)):
        doctor_img = DoctorImg()
        doctor_id = get_reg_doctor_id(str(doctor_id_list[i]))
        doctor_img.doctor_id = doctor_id
        doctor_img_url = str(doctor_img_url_list[i])
        doctor_img.doctor_img_remote_path = doctor_img_url
        doctor_img_datas.append(doctor_img)

    return doctor_img_datas