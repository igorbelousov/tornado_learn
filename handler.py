#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
basedir = os.path.abspath(os.path.dirname(__file__))
import random
from models import Article, User, PostCategory, db_session, Test
from sqlalchemy import desc

from wtforms_alchemy import ModelForm, ModelFormField, ModelFieldList
from wtforms.fields import FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#views
__UPLOADS__ =  os.path.join('media/images/')

class BaseHandler(tornado.web.RequestHandler):
    @tornado.web.removeslash
    def get_current_user(self):
        return self.get_secure_cookie("mechtari")

    
class TForm(ModelForm):
    class Meta:
        model = Test
    
class HomeHandler(BaseHandler):
    
    def get(self):
        form = TForm()
        self.render("home.html", form=form)
        
    def post(self):
        arg = self.request.arguments
        form = TForm()
        print (arg)
        if form.validate():
            self.write('Hello ' )
        else:
            self.render("home.html", form=form)
        
class BlogListHandler(BaseHandler):
    
    def get(self):
        articles = Article.query.order_by(desc(Article.timestamp)).all()
        self.render("blog/list-blog.html", articles=articles)        

class BlogPageHandler(BaseHandler):
    
    def get(self):
       
        self.render("blog/blog-page.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")        
# 
# class HomeHandler(BaseHandler):
#     
#     def get(self):
#        
#         self.render("home.html")


#admin views
class CForm(ModelForm):
    class Meta:
        model = PostCategory
        
    

class AForm(ModelForm):
    def enabled_categories():
        return PostCategory.query.all()
    
    def enabled_users():
        return User.query.all()

    class Meta:
        model = Article
        
    category = QuerySelectField(query_factory=enabled_categories,
                                allow_blank=True)
    author = QuerySelectField(query_factory=enabled_users,
                                allow_blank=True)
    
class AdminBlogList(BaseHandler):
    def get(self):
        articles = Article.query.order_by(desc(Article.timestamp)).all()
        
        self.render("admin/blog/list-blog.html", articles=articles )
        
class AdminArticle(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        article = None
        form = AForm()
        if id:
            article = Article.query.filter_by(id = int(id)).one()
            form = AForm(obj = article)
        self.render("admin/blog/blog-page.html", article=article, form=form)
        
    def post(self):
        form = AForm()
        
        id = self.get_argument('id', None)
        title = self.get_argument('title')
        slug = self.get_argument('slug')
        category_id = self.get_argument('category')
        content = self.get_argument('content')
        author_id = self.get_argument('author')
        description = self.get_argument('description')
        seo_description = self.get_argument('seo_description')
        seo_keywords = self.get_argument('seo_keywords')
        seo_title = self.get_argument('seo_title')
        
        try:
            f = self.request.files['file1'][0]
            image = f['filename']
            extn = os.path.splitext(image)[1]
            if extn in ('.jpg','.png','.bmp','.jpeg'):
                name =str(int(random.random()*10000000000000))
                fh = open(__UPLOADS__ + name + extn, 'w')
                fh.write(f['body'])
                image = name+extn
            else:
                self.finish('this is is not image file')
        except:
            image = self.get_argument('image')

        
        if form.validate():
            if id:
                ar = Article.query.filter_by(id=id).one()
                if not ar: raise tornado.web.HTTPError(404)
                ar.title = title
                ar.slug = slug
                ar.category_id = category_id
                ar.content = content
                ar.author_id = author_id
                ar.description = description
                ar.image = image
                ar.seo_description = seo_description
                ar.seo_keywords = seo_keywords
                ar.seo_title = seo_title
                db_session.add(ar)
                db_session.commit()

                self.redirect('/manage/articles')
            else:
                while True:
                    e = Article.query.filter_by(slug=slug).first()
                    if not e: break
                    slug += "-2"
                ar = Article(title,  slug, category_id, content, author_id, description, image, seo_description, seo_keywords, seo_title)
                db_session.add(ar)
                try:
                    db_session.commit()
                except:
                    db_session.rollback()

                self.redirect('/manage/articles')
                
        else:
            self.write('eror')
