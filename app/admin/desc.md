
这里的这个login_required装饰器就是我们对该视图进行了验证，只有登录的用户才可以访问！


进行分页查询：
通过order_by()方法按照发布时间进行倒序排列，
在使用paginate()方法进行分页，per_page=10代表每页显示数量，超过该设置的数量则进行分页，
error_out=False代表是否访问不存在的分页时显示错误页面，False是不显示！


category_list :分页列表