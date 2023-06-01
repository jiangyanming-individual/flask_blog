# author:Lenovo
# datetime:2023/5/1 15:28
# software: PyCharm
# project:flask_blog


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

SECRET_KEY = 'jiangyanming'

"""数据库的配置路径："""
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flask_blog?charset=utf8'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True