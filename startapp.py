#!/usr/bin/env python
import os.path
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from handler import HomeHandler, BlogListHandler, BlogPageHandler, AdminBlogList, AdminArticle 




basedir = os.path.abspath(os.path.dirname(__file__))


application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/blog", BlogListHandler),
    (r"/blog/page", BlogPageHandler),
    
    (r"/manage/articles", AdminBlogList),
    (r"/manage/article", AdminArticle)

],
    template_path=os.path.join(basedir, "templates"),
    static_path=os.path.join(basedir, "media"),
    xsrf_cookies=True,
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    login_url= "/login",
    debug=True )



#starter
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

