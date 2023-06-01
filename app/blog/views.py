# author:Lenovo
# datetime:2023/5/1 15:49
# software: PyCharm
# project:flask_blog

from flask import Blueprint,render_template,request
from app.blog.models import Post,Category,Tag
import random

bp = Blueprint('blog', __name__, url_prefix='/blog',static_folder='static',template_folder='templates')

@bp.route('/index')
def index():

    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(-Post.add_date).paginate(page=page,per_page=9,error_out=False)
    post_list=pagination.items

    imgs = ['https://ts1.cn.mm.bing.net/th/id/R-C.b022d8b413424e50971daeee8df46006?rik=03p8iIp%2bzvd6xQ&riu=http%3a%2f%2fpic7.nipic.com%2f20100517%2f2183716_141932054953_2.jpg&ehk=ZL1w5l3Rs9ya3zYGA1TWYXMwAVA1B6iIXnI0ly1d3LE%3d&risl=&pid=ImgRaw&r=0',
            'https://pic1.zhimg.com/v2-e915686432f3bb45dd43705ec445352d_r.jpg',
            'https://ts1.cn.mm.bing.net/th/id/R-C.a16d51f94a16d30f62ecdf92be36eb70?rik=fCVMw%2bFPByppBw&riu=http%3a%2f%2fwww.kutoo8.com%2fupload%2fimage%2f60402689%2f20170710002.jpg&ehk=J5JO72TS1ZmdxDJF5z4WtaQoV0LwtSW3EeiWv4aoW0k%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.009dbb0af094705ed3632bae90378730?rik=3z09sHbE%2bT%2fgRg&riu=http%3a%2f%2fpic.bizhi360.com%2fbbpic%2f35%2f8035.jpg&ehk=jRXHXPr3qu67DYFwiOxPAAWBpu1xjbkeoKj3x6ykQqw%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.f8e5d218d29d0343b2f4811e1d1102c7?rik=yJwoN46shAM15w&riu=http%3a%2f%2fpic4.bbzhi.com%2ffengjingbizhi%2fwaiguoziranfengjingzhuomianbizhi%2fwaiguoziranfengjingzhuomianbizhi_405111_5.jpg&ehk=Qxw0LiYdelKhoy6fOFoP8sO8xRrayewQU2MaaKJxOMc%3d&risl=&pid=ImgRaw&r=0',
            'https://statics.888ppt.com/Upload/photothumb/bx12Nqd1kNk.jpg!w800',
            'https://ts1.cn.mm.bing.net/th/id/R-C.8d53df2d59b55efe59eaa4eb7187b359?rik=%2b9R9%2bT%2fHawXnMQ&riu=http%3a%2f%2fpic.qqbizhi.com%2fallimg%2fbbpic%2f73%2f973_6.jpg&ehk=zuyXbAtcpjXWL%2b%2bze3lwhVLddoeomp8AgaDtg7UVR5g%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.f1e812793db01f91d2f3c3ba3170e9b2?rik=wWVRN0nDp7vIYw&riu=http%3a%2f%2fpic.bizhi360.com%2fbbpic%2f72%2f6572.jpg&ehk=Jofon8hSdAuGUWZlfcJuSvncnsYZsKv0KdGjxHD%2b2eg%3d&risl=&pid=ImgRaw&r=0',
            'https://www.euweb.cn/wp-content/uploads/2016/12/302636-106.jpg',
            'https://ts1.cn.mm.bing.net/th/id/R-C.aac15df2528246b0794b422f5f588fd2?rik=jWQkodCBbbDx7A&riu=http%3a%2f%2fi.52desktop.cn%3a81%2fupimg%2fallimg%2f20110224%2f2011224145510844778018.jpg&ehk=BgvDnJlJ%2btOdePpnWjQwwwgmLWabOsoQFT6L0Qn1V00%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.af95b71983f44268bd35b7af7d0f5a47?rik=aGkRkAbl1eZeeg&riu=http%3a%2f%2fup.deskcity.org%2fpic_source%2faf%2f95%2fb7%2faf95b71983f44268bd35b7af7d0f5a47.jpg&ehk=KTrjD374omtlZgCss8t%2fFYMkLiJrtKIM3m9bmr5ujvw%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.a390c5f36f23fb0af1e4a34a497ab0d3?rik=MQfbHkg062xWFQ&riu=http%3a%2f%2fimg.mm4000.com%2ffile%2f6%2f33%2fcbc8d79b0b.jpg&ehk=kIwHRN6Lo9fxCJOaRczYBQE4UDrxsufDs6wTvTjhxQA%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.e5a539b8e7ca600877cea25c9d05f619?rik=%2fblIPTajzKLc%2fw&riu=http%3a%2f%2fimg.pconline.com.cn%2fimages%2fupload%2fupc%2ftx%2fwallpaper%2f1209%2f13%2fc0%2f13827288_1347505315557.jpg&ehk=ESrchnqlrZ8mFnlxb%2fEguJk%2fVi718P4eRr5PRd8o4M4%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.0e8481bc92b279810c4893dfc9bbb50f?rik=E9U4ghlIxjB%2fuQ&riu=http%3a%2f%2fpica.nipic.com%2f2008-01-09%2f200819115558772_2.jpg&ehk=qwNEbO%2fBUt6BByiOObWneCtICC53UFmRbx1yPqaeFb4%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.6d01d968b81986b1d9bfc90821a8b482?rik=%2fWZTmTrMFJwdMg&riu=http%3a%2f%2fimg.mm4000.com%2ffile%2f4%2f13%2f3d0fb7e7c3.jpg&ehk=yMIR6KdXXX%2f9k6glX%2b97HEDVYK2R%2bj8pt5z5rtxaSws%3d&risl=&pid=ImgRaw&r=0',
            'https://ts1.cn.mm.bing.net/th/id/R-C.0701ee8920316eaacfc9ed0990635148?rik=G%2b%2b7p2mQYkooxg&riu=http%3a%2f%2fwww.pptbz.com%2fpptpic%2fUploadFiles_6909%2f201406%2f2014062420035560.jpg&ehk=uyVZ1ylTKT%2bvCmd9lb0l3x5xhTmXOq6poLscKE1eeMM%3d&risl=&pid=ImgRaw&r=0',
            ]
    for post in post_list:
        post.img=random.sample(imgs,1)[0]

    return render_template('base.html', posts=post_list,pagination=pagination)


"""分类中的列表详情页"""
@bp.route('/category/<int:cate_id>')
def cates(cate_id):
    #分类页：查看文章列表：
    cate=Category.query.get(cate_id)
    page=request.args.get('page',1,type=int)
    pagination=Post.query.filter(Post.category_id == cate.id).paginate(page=page,per_page=10,error_out=False)
    post_list=pagination.items


    return render_template('cate_list.html',cate=cate,cate_id=cate_id,post_list=post_list,pagination=pagination)



"""实现文章详情页视图"""
@bp.route('/category/<int:cate_id>/<int:post_id>')
def detail(cate_id,post_id):

    cate=Category.query.get(cate_id)
    post=Post.query.get_or_404(post_id)

    #上一篇：查找到prev_post对象；
    prev_post=Post.query.filter(Post.id<post_id).order_by(-Post.id).first()
    # 下一篇：查找next_post对象；

    next_post=Post.query.filter(Post.id>post_id).order_by(-Post.id).first()

    return render_template('detail.html',cate=cate,post=post,prev_post=prev_post,next_post=next_post)




"""实现文章归档的功能,进行上下文的注册"""
@bp.context_processor
def inject_archive():

    posts=Post.query.order_by(Post.add_date)
    #设置日期格式：
    dates=set([post.add_date.strftime("%Y年%m月") for post in posts])

    #标签：
    tags=Tag.query.all()


    for tag in tags:
        tag.style = ['is-success', 'is-danger', 'is-black', 'is-light', 'is-primary', 'is-link', 'is-info',
                     'is-warning']

    #最新文章：
    new_posts=posts.limit(6)

    return dict(dates=dates,tags=tags,new_posts=new_posts)


@bp.route('/category/<string:date>')
def archive(date):
    # 归档页
    import re
    # 正则匹配年月
    regex = re.compile(r'\d{4}|\d{2}')
    dates = regex.findall(date)

    from sqlalchemy import extract, and_, or_
    page = request.args.get('page', 1, type=int)
    # 根据年月获取数据
    archive_posts = Post.query.filter(and_(extract('year', Post.add_date) == int(dates[0]), extract('month', Post.add_date) == int(dates[1])))
    # 对数据进行分页
    pagination = archive_posts.paginate(page=page, per_page=10, error_out=False)
    post_list=pagination.items
    return render_template('archive.html', post_list=post_list,  pagination=pagination, date=date)



"""查找tags标签："""
@bp.route('/tags/<int:tag_id>')
def tags(tag_id):

    tag=Tag.query.get(tag_id) #tag 和 post是多对多的关系：
    return render_template('tags.html',post_list=tag.post,tag=tag)


"""关键字搜索"""
@bp.route('/search')
def search():

    words=request.args.get('words',type=str)
    page=request.args.get('page',1,type=int)
    pagination=Post.query.filter(Post.title.like("%"+words+"%")).paginate(page=page,per_page=10,error_out=False)
    post_list=pagination.items

    return render_template('search.html',post_list=post_list,words=words,pagination=pagination)

