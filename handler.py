#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
basedir = os.path.abspath(os.path.dirname(__file__))
import random
from models import Article, User, PostCategory, db_session 
from sqlalchemy import desc
from wtforms_alchemy import ModelForm, ModelFormField, ModelFieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import IntegerField, StringField, PasswordField, TextField, TextAreaField, SelectField
from wtforms.validators import Required, Optional 
from wtforms_tornado import Form

#views
__UPLOADS__ =  os.path.join('media/images/')

class BaseHandler(tornado.web.RequestHandler):
    
    @tornado.web.removeslash
    def get_current_user(self):
        return self.get_secure_cookie("mechtari")
    
    def initialize(self):
        self.session = db_session()

    def on_finish(self):
        self.session.close()

class HomeHandler(BaseHandler):
    
    def get(self):

        self.render("home.html")  
        
class BlogListHandler(BaseHandler):
    
    def get(self):
        articles = Article.query.order_by(desc(Article.timestamp)).all()
        self.render("blog/list-blog.html", articles=articles)        

class BlogPageHandler(BaseHandler):
    
    def get(self):       
        self.render("blog/blog-page.html")
        
class AForm(ModelForm, Form):
    
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
        form = AForm(self.request.arguments)        
        id = self.get_argument('id', None)        
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
            image = self.get_argument('image', None)
        if form.validate():            
            if id:
                ar = Article.query.filter_by(id=id).one()
                if not ar: raise tornado.web.HTTPError(404)
                form.populate_obj(ar)                
                db_session.add(ar)
                db_session.commit()            
                self.redirect('/manage/articles')
            else:
                while True:
                    e = Article.query.filter_by(slug=form.data['slug']).first()
                    if not e: break
                    form.data['slug'] += "-2"
                ar = Article(1,2,34,12,12)
                form.populate_obj(ar)
                db_session.add(ar)
                try:
                    db_session.commit()
                except:
                    db_session.rollback()
            
                self.redirect('/manage/articles')                
        else:
            self.write('%s' %form.errors)