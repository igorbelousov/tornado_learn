#!/usr/bin/env python
import os.path
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from handler import HomeHandler, BlogListHandler, Qty, ProductsListHandler, CartHandler, LoginHandler, LogoutHandler, ProfileHandler, BlogPageHandler, AdminBlogList, AdminProductList, AdminArticle, ProductAdminHandler 

basedir = os.path.abspath(os.path.dirname(__file__))

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/blog", BlogListHandler),
    (r"/blog/page/([0-9]+)", BlogPageHandler),    
    (r"/manage/articles", AdminBlogList),
    (r"/manage/article", AdminArticle),
    (r"/manage/product", ProductAdminHandler),
    (r"/manage/products", AdminProductList),
    (r"^/products$", ProductsListHandler),
    (r"^/cart$", CartHandler),
    (r"^/login$", LoginHandler),
    (r"^/logout$", LogoutHandler),
    (r"^/profile$", ProfileHandler)

],
    template_path=os.path.join(basedir, "templates"),
    static_path=os.path.join(basedir, "media"),
    ui_modules={'qty': Qty},
    xsrf_cookies=True,
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    login_url= "/login",
    debug=True )

#starter
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()