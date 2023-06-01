# author:Lenovo
# datetime:2023/5/1 15:48
# software: PyCharm
# project:flask_blog

from datetime import datetime
from realproject import db
from enum import IntEnum
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Integer,String,ForeignKey

"""时间基类模型"""
class Base_Model(db.Model):
    __abstract__ = True
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 创建时间
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间


"""文章分类与文章是 1 对多的关系；一个分类下可以有多个文章"""
class Category(Base_Model):
    """
    文章分类模型
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)
    post=db.relationship('Post',backref='category',lazy=True)

    def __repr__(self):
        return '<Category %r>' % self.name




"""文章发布类型;枚举"""
class PostPublishType(IntEnum):
    draft=1 #草稿
    show=2 #发布

'''多对多的表：'''
tags=db.Table(
    'tags_post',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
)

class Post(Base_Model):
    """文章模型"""

    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(128),nullable=False)
    desc=db.Column(db.String(128),nullable=False)
    has_type=db.Column(db.Enum(PostPublishType),server_default='show', nullable=False)
    '''文章分类 1：多 -->文章'''
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    content=db.Column(LONGTEXT, nullable=False) #内容
    '''多对多 ；文章对应文章标签'''
    tags=db.relationship('Tag',secondary=tags,lazy='subquery',backref=db.backref('post',lazy=True)) #lazy ：延迟加载；

    def __repr__(self):
        return f'<Post{self.title}>'



class Tag(Base_Model):
    """文章标签model"""

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(128),nullable=False)

    def __repr__(self):
        return f'<Tag {self.name}>'