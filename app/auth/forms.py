# author:Lenovo
# datetime:2023/5/2 14:25
# software: PyCharm
# project:flask_blog

"""进行用户注册和登录表单的验证"""

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Length,ValidationError,EqualTo
from werkzeug.security import check_password_hash
from .models import  User



class LoginForm(FlaskForm):

    def qs_username(username):
        # 对该字段进行在传递之前处理
        u=f'{username}123456'
        print(u)

        return username


    username=StringField('username',
        validators=[
        DataRequired(message="用户名不能为空!"), #校验字段是否为空
        Length(max=32,message="不符合长度要求!")#校验长度
        ],filters=(qs_username,))
    password=PasswordField('password',
        validators=[
            DataRequired(message="密码不能为空!"),
            Length(max=32,message="不符合长度要求!")
        ])

    def validate_username(form,field):

        user=User.query.filter_by(username=field.data).first()

        if user is None:
            error="该用户不存在！"
            raise ValidationError(error) #抛出错误
        elif not check_password_hash(user.password,form.password.data):
            error="密码错误！"
            raise ValidationError(error)


class RegisterForm(FlaskForm):
    
    #注册表单验证：

    username = StringField('username',
    validators=[
        DataRequired(message="！"),  # 校验字段是否为空
        Length(min=2,max=32, message="不符合长度要求！")  # 校验长度
    ])
    password = PasswordField('password',
    validators=[
        DataRequired(message="密码不能为空!"),
        Length(min=6, max=32, message="不符合长度要求!"),
        EqualTo('checkpassword',message="两次输入密码不一致!")
    ])

    checkpassword=PasswordField('checkpassword')


    def validate_username(form,field):
        user=User.query.filter_by(username=field.data).first()

        if user is not None:
            error="该用户名已经存在！请重新命名！"
            raise ValidationError(error)









