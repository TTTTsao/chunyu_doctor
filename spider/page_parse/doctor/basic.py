from spider.util.reg.reg_doctor import get_reg_doctor_id

from lxml import etree

def get_active_doctor_id_list(html):
    '''
    get active doctor id list
    从【根据科室找医生】获取活跃的医生id list
    :param html:
    :return:
    '''
    if not html: return

    xpath = etree.HTML(html)
    row_doctor_id_list = xpath.xpath("/html/body/div[4]/div[4]/div/div[2]/div[1]/a/@href")
    doctor_id_list = []

    for i in range(len(row_doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(row_doctor_id_list[i]))
        doctor_id_list.append(doctor_id)

    return doctor_id_list

def get_doctor_id_list_from_clinic_page(html):
    '''
    从科室页获取当页的doctor id list
    :param html:
    :return:
    '''
    if not html: return
    xpath = etree.HTML(html)
    row_doctor_id_list = xpath.xpath("//div[@class='avatar-wrap']/a/@href")

    # 判断页面有无医生
    if len(row_doctor_id_list) == 0: return

    doctor_id_list = []
    for i in range(len(row_doctor_id_list)):
        doctor_id = get_reg_doctor_id(str(row_doctor_id_list[i]))
        doctor_id_list.append(doctor_id)

    return doctor_id_list