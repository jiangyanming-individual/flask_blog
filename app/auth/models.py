# author:Lenovo
# datetime:2023/5/1 17:54
# software: PyCharm
# project:flask_blog


"""用户models的编写"""

from datetime import datetime
from realproject import db



class Base_Model(db.Model):
    """基类模型
    """
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, ) # 创建时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # 更新时间

class User(Base_Model):

    """用户模型"""
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(128),unique=True,nullable=False) #用户名唯一
    password=db.Column(db.String(320),nullable=False)
    avatar=db.Column(db.String(200),nullable=True)
    is_super_user=db.Column(db.Boolean,nullable=True,default=False) #是不是超级管理员
    is_active=db.Column(db.Boolean,nullable=True,default=True) #是否为活跃用户
    is_staff=db.Column(db.Boolean,nullable=True,default=False) # 是否允许登录后台
    gexing=db.Column(db.String(100),nullable=True) #个性签名；
    desc=db.Column(db.String(150),nullable=True)  #个人简介
    gender=db.Column(db.String(30),nullable=True)
    email=db.Column(db.String(100),nullable=True)
    address=db.Column(db.String(150),nullable=True)


    def __repr__(self):
        return '<Category %r>'%self.username


