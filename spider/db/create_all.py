import sys

# to work well inside config module or outsize config module
sys.path.append('..')
sys.path.append('.')

from spider.db.tables import *
from spider.db.basic import metadata


def create_all_table():
    metadata.create_all()


if __name__ == "__main__":
    create_all_table()