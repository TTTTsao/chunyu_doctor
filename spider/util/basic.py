import datetime


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

if __name__ == '__main__':
    time_str = '2022-11-09'
    print(trans_to_datetime(time_str))