# author:Lenovo
# datetime:2023/5/2 15:27
# software: PyCharm
# project:flask_blog

from unicodedata import name
from flask import Blueprint, flash, redirect, render_template, request, url_for, g
from app.auth.views import login_required
from realproject import db
from app.blog.models import Category,Post,Tag
from app.auth.models import User
from app.admin.forms import CategotyCreateForm,PostForm,TagForm,CreateUserForm
from werkzeug.security import check_password_hash,generate_password_hash
from app.admin.utils import upload_file_path


bp=Blueprint('admin',__name__,url_prefix='/admin',static_folder='static',template_folder='templates')



"""管理员登录首页"""
@bp.route('/')
@login_required
def index():
    #个人主后台主页面
    return render_template('admin/index.html')



"""文章分类查询"""
@bp.route('/category')
@login_required
def category():
    page = request.args.get('page', 1, type=int)
    #坑点：page=page
    pagination = Category.query.order_by(-Category.add_date).paginate(page=page, per_page=10,error_out=False)
    category_list = pagination.items
    return render_template('admin/category.html',category_list=category_list, pagination=pagination)



"""文章分类添加"""
@bp.route('/category/add',methods=['POST','GET'])
@login_required
def category_add():

    #增加分类:
    form=CategotyCreateForm()

    if form.validate_on_submit():
        category=Category(name=form.name.data,icon=form.icon.data)
        db.session.add(category)
        db.session.commit()

        flash(f"{form.name.data}分类添加成功!")
        return redirect(url_for('admin.category')) #添加成功跳转到admin/category页面

    return render_template('admin/category_form.html',form=form) #跳转到添加页面;



"""文章分类编辑:需要回显数据"""
@bp.route('/category/edit/<int:cate_id>',methods=['POST','GET'])
@login_required
def category_edit(cate_id):
    #编辑分类:

    category=Category.query.get(cate_id) #先数据库中查询数据
    form=CategotyCreateForm(name=category.name,icon=category.icon)

    if form.validate_on_submit():

        category.name=form.name.data
        category.icon=form.icon.data

        db.session.add(category)
        db.session.commit()

        flash(f"{form.name.data}编辑完成!")

        return redirect(url_for('admin.category'))

    return render_template('admin/category_form.html',form=form)

"""文章分类删除:需要回显数据"""
@bp.route('/category/delete/<int:cate_id>',methods=['POST','GET'])
@login_required
def category_delete(cate_id):

    #文章分类删除:
    category=Category.query.get(cate_id)

    if category:
        db.session.delete(category)
        db.session.commit()

        flash(f"{category.name}删除完成!")
        return redirect(url_for('admin.category'))




"""文章管理首页"""
@bp.route('/article')
@login_required
def article():
    #查看文章:
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(-Post.add_date).paginate(page=page,per_page=10,error_out=False)
    post_list=pagination.items

    return render_template('admin/article.html',post_list=post_list,pagination=pagination)


"""文章管理添加页"""
@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 增加文章
    form = PostForm()
    form.category_id.choices=[(cate.id,cate.name)for cate in Category.query.all()]
    form.tags.choices=[(tag.id,tag.name)for tag in Tag.query.all()]

    if form.validate_on_submit():
        post=Post(
            title=form.title.data,
            desc=form.desc.data,
            has_type=form.has_type.data,
            category_id=int(form.category_id.data),
            content=form.content.data,
        )
        post.tags=[Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()

        flash(f"{form.title.data}文章添加成功!")
        return redirect(url_for('admin.article'))

    return render_template('admin/article_form.html',form=form)


"""文章管理修改页"""
@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 修改文章
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]
    form = PostForm(
        title=post.title,
        desc=post.desc,
        category_id=post.category.id,
        has_type=post.has_type.value,
        content=post.content,
        tags=tags
    )
    form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id=int(form.category_id.data)
        post.content = form.content.data
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章修改成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)



"""删除文章"""
@bp.route('/article/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_delete(post_id):

    post=Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash(f"{post.title}文章删除完成!")

        return redirect(url_for('admin.article'))


"""展示标签"""
@bp.route('/tag')
@login_required
def tag():
    #查看标签列表：

    page=request.args.get('page',1,type=int)
    pagination=Tag.query.order_by(-Tag.add_date).paginate(page=page,per_page=10,error_out=False)
    tag_list=pagination.items

    return render_template('admin/tag.html',tag_list=tag_list,pagination=pagination)

"""添加标签"""
@bp.route('/tag/add',methods=['POST','GET'])
@login_required
def tag_add():
    #添加新的tag
    form=TagForm()
    if form.validate_on_submit():
        tag=Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()

        flash(f'{form.name.data}标签添加成功！')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html',form=form)


"""编辑标签"""
@bp.route('/tag/edit/<int:tag_id>',methods=['POST','GET'])
@login_required
def tag_edit(tag_id):

    tag=Tag.query.get(tag_id)#查数据
    form=TagForm(name=tag.name) #回显数据

    if form.validate_on_submit():
        tag.name=form.name.data
        db.session.add(tag)
        db.session.commit()

        flash(f'{form.name.data}标签编辑完成！')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html',form=form)



"""编辑标签"""
@bp.route('/tag/delete/<int:tag_id>',methods=['POST','GET'])
@login_required
def tag_delete(tag_id):

    tag=Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()

        flash(f'{tag.name}删除完成！')
        return redirect(url_for('admin.tag'))



@bp.route('/user')
@login_required
def user():
    #查看用户
    page=request.args.get('page',1,type=int)
    pagination=User.query.order_by(-User.add_date).paginate(page=page,per_page=10,error_out=False)
    user_list=pagination.items

    return render_template('admin/user.html',user_list=user_list,pagination=pagination)




@bp.route('/user/add',methods=['POST','GET'])
@login_required
def user_add():

    from app.admin.utils import upload_file_path
    form=CreateUserForm()

    if form.validate_on_submit():
        f=form.avatar.data
        avatar_path,filename=upload_file_path('avatar',f)
        f.save(avatar_path) #保存文件图片；

        user=User(
            username=form.username.data,
            password=generate_password_hash(form.password.data),#加密
            avatar=f'avatar/{filename}',#存放的是路径：
            is_super_user=form.is_super_user.data,
            is_active=form.is_active.data,
            is_staff=form.is_staff.data
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('admin.user'))

    return render_template('admin/user_form.html',form=form)


@bp.route('/user/edit/<int:user_id>',methods=['POST','GET'])
@login_required

def user_edit(user_id):

    user=User.query.get(user_id)

    from app.admin.utils import upload_file_path

    form=CreateUserForm(
        username=user.username,
        password=user.password,
        avatar=user.avatar,
        is_super_user=user.is_super_user,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    print(form.is_super_user.data)
    form.password.default=f'{user.password}'

    if form.validate_on_submit():
        user.username=form.username.data,
        if not form.password.data:#没有修改密码
            user.password=user.password
        else:
            user.password=generate_password_hash(form.password.data)

        f=form.avatar.data
        if user.avatar == f: #没有修改图片；
            user.avatar=user.avatar
        else:
            avatar_path,filename=upload_file_path('avatar',f)
            f.save(avatar_path)
            user.avatar=f'avatar/{filename}'

        user.is_super_user=form.is_super_user.data
        user.is_active=form.is_active.data
        user.is_staff=form.is_staff.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.user'))

    return render_template('admin/user_form.html',form=form,user=user) #还需要传递user


@bp.route('/user/del/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_delete(user_id):

    user=User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('admin.user'))


@bp.route('/userinfo/edit',methods=['POST','GET'])
@login_required
def userinfo_edit():
    user=User.query.get(g.user.id)
    #修改个人信息，但不修改权限：
    form=CreateUserForm(
        username=user.username,
        password=user.password,
        avatar=user.avatar,
        gexing=user.gexing,
        desc=user.desc,
        email=user.email,
        gender=user.gender,
        address=user.address
    )

    if form.validate_on_submit():
        user.username = g.user.username

        if not form.password.data:
            user.password=user.password
        else:
            user.password=generate_password_hash(form.password.data)

        from app.admin.utils import upload_file_path
        f=form.avatar.data

        if user.avatar == f:
            #不修改头像：
            user.avatar= user.avatar
        else:
            avatar_path,filename=upload_file_path('avatar',f)
            f.save(avatar_path)
            user.avatar=f'avatar/{filename}' #修改头像：

        user.gexing=form.gexing.data
        user.desc=form.desc.data
        user.gender=form.gender.data
        user.email=form.email.data
        user.address=form.address.data

        db.session.add(user)
        db.session.commit()

        flash(f'{user.username}个人信息修改成功！')
        return redirect(url_for('auth.userinfo'))
    return render_template('userinfo_edit.html',form=form)


@bp.route('/upload',methods=['POST','GET'])
@login_required
def upload():

    #上传图片：
    if request.method == 'POST':
        f=request.files.get('upload')
        file_size=len(f.read())
        f.seek(0)

        if file_size>2048000:
            return {
                'code':'err',
                'message':'文件大小限制2M'
            }

        upload_path,filename=upload_file_path('upload',f)
        f.save(upload_path)

        return {
            'code':'ok',
            'url':f'/admin/static/upload/{filename}'
        }

