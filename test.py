from spider.db.basic import session_scope

import json

if __name__ == '__main__':
    # with session_scope() as session:
    #     result = session.execute("select distinct hospital_id from raw_hospital")
    #     id_list = [item[0] for item in result]
    #     with open("hospital_id_little.json", "w") as f:
    #         f.write(json.dumps(id_list))
    with open("hospital_id_little.json", "r") as f:
        result = json.load(f)
        print(type(result))
