from spider.db.basic import session_scope
import json

def init_id():
    with session_scope() as session:
        doctor_result = session.execute("select distinct doctor_id from raw_doctor_base_info")
        doctor_id_list = [item[0] for item in doctor_result]
        with open("../../../doctor_id.json", "w") as f:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(doctor_id_list))

        hospital_result = session.execute("select distinct hospital_id from raw_hospital")
        hospital_id_list = [item[0] for item in hospital_result]
        with open("../../../hospital_id.json", "w") as f:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(hospital_id_list))

if __name__ == '__main__':
    init_id()