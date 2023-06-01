# author:Lenovo
# datetime:2023/5/2 15:27
# software: PyCharm
# project:flask_blog



from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,RadioField,SelectField,SelectMultipleField,TextAreaField,PasswordField,EmailField
from wtforms.validators import DataRequired,Length
from app.blog.models import PostPublishType
#上传文件：
from flask_wtf.file import FileField,FileRequired,FileSize,FileAllowed

"""进行文章分类表单的校验"""
class CategotyCreateForm(FlaskForm):

    #分类表单:
    name=StringField('分类名称',
        validators=[
            DataRequired(message="内容不能为空!"),
            Length(max=128,message="不符合长度要求!")
        ])
    icon=StringField('分类图标',
        validators=[
        Length(max=256,message="长度不符合要求!")
    ])





"""进行文章表单的校验"""
class PostForm(FlaskForm):
    # 添加文章表单
    title = StringField('标题', validators=[
        DataRequired(message="不能为空"),
        Length(max=128, message="不符合字数要求！")
    ])
    desc = StringField('描述', validators=[
        DataRequired(message="不能为空"),
        Length(max=200, message="不符合字数要求！")
    ])
    # RadioField也就是单选按钮表单
    has_type = RadioField('发布状态',
        choices=(PostPublishType.draft.name, PostPublishType.show.name),
        default=PostPublishType.show.name)

    # SelectField是下拉表单类;，choices是选项，coerce定义该表单值得类型，默认为str
    category_id = SelectField(
        '分类',
        choices=None,
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ]
    )
    # TextAreaField则是多行输入表单
    content = TextAreaField('文章详情',
        validators=[DataRequired(message="不能为空")]
    )

    # SelectMultipleField多选表单，其他参数均与SelectField一致
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)


"""创建tag表单"""

class TagForm(FlaskForm):

    name=StringField('标签',validators=[
        DataRequired(message="不能为空！"),
        Length(max=128,message="不和长度要求！")
    ])



"""进行用户的表单的校验"""

class CreateUserForm(FlaskForm):

    username=StringField('username',validators=[
        DataRequired(message="不能为空！"),
        Length(max=32,message="长度不符合要求")
    ])
    password=PasswordField('password',validators=[
        Length(max=32,message="长度不符合要求"),
    ],description="修改用户信息时，留空则代表不修改！")

    avatar=FileField('avatar',validators=[
        FileAllowed(['jpg','png','gif'],message="仅支持jpg,png,gif格式"),
        FileSize(max_size=2048000,message="不能大于2M")
    ],description="修改用户信息时，留空则代表不修改！")

    is_super_user=BooleanField('是否为管理员')
    is_active=BooleanField('是否活跃',default=True)
    is_staff=BooleanField('是否锁定')

    gexing=StringField('个性签名',validators=[
        Length(max=100,message="长度不符合要求！")
    ])
    desc=StringField('desc',validators=[
        Length(max=150,message="长度不符合要求！")
    ])
    email=EmailField('邮箱')
    gender=SelectField('性别',choices=(('man','男'),('woman','女')))
    address=StringField('地址',validators=[
        Length(max=150,message="长度不符合要求！")
    ])