****index.html 是基类模板;是一个form表单****

1.register.html 是继承了index.html

2.models存放了User模型

3.views是 视图函数:包括login;register函数的功能；

这里用到了一个check_password_hash()的方法，
这是用来将密文密码解密后与用户输入密码比对方法，
与之对应的有一个generate_password_hash()的方法用来加密明文密码保存到数据库！


4.forms是对表单进行验证；

5 if form.validate_on_submit(): 验证前端传递的数据是否有效，并且会自动判断是POST请求还是GET请求！

{{ form.csrf_token }} ccsrf验证
{{ form.username(class='input', placeholder='Username') }} 这样就可以直接获得一个表单html并自动渲染，
向该表单增加书香的方式就是像代码中这样传入参数和值即可，
当然也可以提前在表单类中定义！

return render_template('register.html',form=form) #传递form到前端
