# author:Lenovo
# datetime:2023/5/4 19:34
# software: PyCharm
# project:flask_blog


"""
自定义的文件上传的函数
"""

import os
import uuid
from realproject.settings import BASE_DIR
from werkzeug.utils import secure_filename


def _file_path(dir_name):

    file_path=BASE_DIR/f'app/admin/static/{dir_name}'
    #判断路劲是否存在
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)

    return file_path


def upload_filename(f):
    #修改文件名：
    names=list(os.path.splitext(secure_filename(f.filename)))
    names[0]=''.join(str(uuid.uuid4()).split('-'))

    return ''.join(names)


def upload_file_path(dir_name,f):

    #构造上传的路径：
    file_path=_file_path(dir_name)
    filename=upload_filename(f)

    return file_path/filename,filename
