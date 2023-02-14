import datetime
from spider.db.basic import session_scope

def get_datetime():
    time_now = datetime.datetime.today()
    return time_now

def trans_to_datetime(str):
    '''
    将string格式的时间转为Datetime
    :param str:
    :return:
    '''
    datetime_time = datetime.datetime.strptime(str, '%Y-%m-%d')
    return datetime_time

def check_db_interval(table_name, conditions, interval_hours):
    '''
    数据库记录检查，距离现在多少时间内是否存在记录
    :param table_name: 表名
    :param conditions: 条件值{k:'', v:''}
    :param interval_hours: 距离目前相距多少小时内
    :return: 距离目前相距多少小时内是否存在记录
    '''
    conditions_sql_list = [str(item['k']) + " = '%s'" % (str(item['v'])) for item in conditions]
    conditions_sql_list.append(
        "updated_at > '%s'" % str(datetime.datetime.now() + datetime.timedelta(hours=-interval_hours)))
    check_condition_sql = "SELECT 1 FROM %s WHERE %s LIMIT 0,1" % (table_name, " AND ".join(conditions_sql_list))
    with session_scope() as session:
        results = session.execute(check_condition_sql)
        return len(results.fetchall()) > 0

def check_db_today(table_name, conditions):
    '''
    数据库记录检查，今天是否存在记录
    :param table_name: 表名
    :param conditions: 条件值{k:'', v:''}
    :return: 今天是否存在记录
    '''
    conditions_sql_list = [str(item['k']) + " = '%s'" % (str(item['v'])) for item in conditions]
    conditions_sql_list.append(
        "created_at > '%s'" % str(datetime.datetime.combine(datetime.date.today(), datetime.time.min)))
    check_condition_sql = "SELECT 1 FROM %s WHERE %s LIMIT 0,1" % (table_name, " AND ".join(conditions_sql_list))
    with session_scope() as session:
        results = session.execute(check_condition_sql)
        return len(results.fetchall()) > 0


def check_db_exist(table_name, conditions):
    '''
    数据库记录检查，是否存在记录
    :param table_name: 表名
    :param conditions: 条件值{k:'', v:''}
    :return: 是否存在记录
    '''
    conditions_sql_list = [str(item['k']) + " = '%s'" % (str(item['v'])) for item in conditions]
    check_condition_sql = "SELECT 1 FROM %s WHERE %s LIMIT 0,1" % (table_name, " AND ".join(conditions_sql_list))
    with session_scope() as session:
        results = session.execute(check_condition_sql)
        return len(results.fetchall()) > 0