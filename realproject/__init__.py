# author:Lenovo
# datetime:2023/5/1 15:26
# software: PyCharm
# project:flask_blog

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from realproject.settings import BASE_DIR
from flask_migrate import Migrate
import os

db= SQLAlchemy()
migrate=Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        CONFIG_PATH = BASE_DIR /'realproject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # test_config为一个字典
        app.config.from_mapping(test_config)


    #初始化数据库：
    db.init_app(app)
    #数据库迁移
    migrate.init_app(app,db)

    # 递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #注册blog蓝图
    from app.blog import views as blog
    app.register_blueprint(blog.bp)

    # 注册auth用户蓝图
    from app.auth import views as auth
    app.register_blueprint(auth.bp)

    # 注册admin用户蓝图
    from app.admin import views as admin
    app.register_blueprint(admin.bp)



    """首页url引入 绑定view_func视图函数"""
    # 端口endpoint参数是该url的端点，类似于django的name参数，
    # 它的作用是方便反查该url，
    # 一般的加载解析顺序是访问该url会先找该端点再找其关联的视图，
    # 然后开始处理逻辑，相当于url的id;
    app.add_url_rule('/',endpoint='index',view_func=blog.index)


    #注册models
    from app.blog import models
    from app.auth import models

    #全局上下文呢：

    app.context_processor(inject_category)

    return app


def inject_category():
    #上下文处理器函数：
    """上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并："""
    from app.blog.models import Category
    categorys=Category.query.limit(6).all()

    return dict(categorys=categorys)