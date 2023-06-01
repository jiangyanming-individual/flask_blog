# author:Lenovo
# datetime:2023/5/1 17:54
# software: PyCharm
# project:flask_blog
import functools
from flask import Flask, Blueprint,render_template,redirect,url_for,request,session,flash,g
from .models import User
#进行加密和解密的方法：
from werkzeug.security import check_password_hash,generate_password_hash
from realproject import db
from .forms import LoginForm,RegisterForm




bp=Blueprint('auth',__name__,url_prefix='/auth',static_folder='static',template_folder='templates')



"""在模板中获取用户信息"""
@bp.before_app_request
def load_logged_in_user():

    #普通用户能够查看的url
    urls=['/auth/','admin/userinfo/edit']

    #在session中找到用户信息：
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get(int(user_id)) #到数据库中找到user的信息：

        #权限判断：

        #管理员：
        if g.user.is_super_user and g.user.is_active:
            g.user.has_prem=1
        #普通用户
        elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request.path in urls:
            g.user.has_prem=1
        #游客
        else:
            g.user.has_prem=0



"""权限访问"""
def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            #给登录添加一个上次访问的url
            redirect_to=f"{url_for('auth.login')}?redirect_to={request.path}"
            return  redirect(redirect_to)

        if g.user.has_prem:
            pass
        else:
            return '<h1>无权查看</h1>'
        return view(**kwargs)

    return wrapped_view



#因为提交的都是for表单，所以使用post方式

@bp.route('/login',methods=['GET','POST'])
def login():


    form =LoginForm()

    #password需要解密；
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        session.clear()
        session['user_id']=user.id
        return redirect(url_for('index'))
    return render_template('login.html',form=form)



@bp.route('/register',methods=['GET','POST'])
def register():

    form=RegisterForm()

    if form.validate_on_submit():
        # 用户信息脱敏,提交数据库
        user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        #注册session
        session.clear()
        session['user_id']=user.id
        #注册成功跳转登录页面：
        return redirect(url_for('auth.login')) #跳转到login函数
    return render_template('register.html',form=form) #传递form到前端

"""退出"""
@bp.route('logout')
def logout():

    session.clear()
    return redirect(url_for('index'))



@bp.route('/')
@login_required
def userinfo():

    #用户中心：
    return render_template('userinfo.html')










