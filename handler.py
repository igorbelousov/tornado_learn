#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
basedir = os.path.abspath(os.path.dirname(__file__))
import random
from models import Article, User, PostCategory, Brand, Category, Product, Series, Cart, OrderItem, db_session 
from sqlalchemy import desc
from wtforms_alchemy import ModelForm, ModelFormField, ModelFieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import IntegerField, StringField, PasswordField, TextField, TextAreaField, SelectField, FileField
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
        
        
def get_user(self):
    email = self.get_argument("mail")
    password = self.get_argument("password")
    if email:
        user = User.query.filter_by(email=email).first()
        if not user:
            self.render("login.html",  user="noname")
        
        if not user.password == password:
            self.render("login.html", user="no password")
            
        if user.role == 1:
            self.set_secure_cookie("mechtari", '%s'% user.id)
            self.set_cookie("user", '%s'% user.id)
            # self.set_cookie(name='user', value='%s' %user.id)
            self.redirect("/manage")
        else:
            self.set_cookie("user", '%s'% user.id)
            self.redirect("/")
            
         
        
def cart(self):
    item = self.get_argument('item')
    cart_id = self.get_cookie('cart_id')
    user = self.get_cookie('user')
    if not cart_id:
        c = Cart(user_id = user)
        db_session.add(c)
        db_session.commit()
        self.set_cookie('cart_id', '%d' % c.id)
        cart_id = c.id
    cart = Cart.query.filter_by(id = int(cart_id)).one()
    # print  "----", cart_id
    if item:
        product = Product.query.filter_by(id = int(item)).one()
    qty = self.get_argument('qty')
    a = OrderItem.query.filter_by(cart_id = int(cart.id), item_id = int(product.id)).first()
    if a:
        a.qty = qty
    else: a = OrderItem(item_id = product.id, cart_id=int(cart.id), qty = qty)
    db_session.add(a)
    db_session.commit()
        
        
  

class HomeHandler(BaseHandler):
    
    def get(self):

        self.render("home.html")
        
        
class ProductForm(ModelForm, Form):
    
    def enabled_categories():
        return Category.query.all()
    
    def enabled_serie():
        return Series.query.all()
    
    def enabled_brand():
        return Brand.query.all()
    class Meta:
        model = Product

    category = QuerySelectField(query_factory=enabled_categories,
                                allow_blank=True)
    series = QuerySelectField(query_factory=enabled_serie,
                                allow_blank=True)
    brand = QuerySelectField(query_factory=enabled_brand,
                                allow_blank=True)
    
    image = FileField()
    
class ProductAdminHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        product = None
        form = ProductForm()
        if id:
            product = Product.query.filter_by(id = int(id)).one()
            form = ProductForm(obj = product) 
        self.render("admin/shop/product-page.html", product=product, form=form)
        
    def post(self):              
        form = ProductForm(self.request.arguments)        
        id = self.get_argument('id', None)
        
        try:
            f = self.request.files['image'][0]
            image = f['filename']
            extn = os.path.splitext(image)[1]
            if extn in ('.jpg','.png','.bmp','.jpeg'):
                name =str(int(random.random()*10000000000000))
                fh = open(__UPLOADS__ + name + extn, 'wb')
                fh.write(f['body'])
                image = name+extn
                
    
            else:
                self.finish('this is is not image file')
        except:
            image = self.get_argument('image', None)
        if form.validate():
            form.image.data = image 
            print(form.image.data )  
            if id:
                ar = Product.query.filter_by(id=id).one()
                if not ar: raise tornado.web.HTTPError(404)
                form.populate_obj(ar)                
                db_session.add(ar)
                db_session.commit()            
                self.redirect('/manage/products')
            else:
                while True:
                    e = Product.query.filter_by(slug=form.data['slug']).first()
                    if not e: break
                    form.data['slug'] += "-2"
                ar = Product(1,2,34,12,12,2,12,131,12,12)
                form.populate_obj(ar)
                db_session.add(ar)
                try:
                    db_session.commit()
                except:
                    db_session.rollback()
            
                self.redirect('/manage/products')                
        else:
            self.write('%s' %form.errors)
            
class AdminProductList(BaseHandler):
    
    def get(self):
        product = Product.query.order_by(desc(Product.id)).all()        
        self.render("admin/shop/products-list.html", product=product )
  
        
class BlogListHandler(BaseHandler):
    
    def get(self):
        articles = Article.query.order_by(desc(Article.timestamp)).all()
        self.render("blog/list-blog.html", articles=articles)        

class BlogPageHandler(BaseHandler):
    
    def get(self, id):
        post = Article.query.filter_by(id=id).one()
        self.render("blog/blog-page.html", post=post)
        
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
    
    image = FileField()
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
            f = self.request.files['image'][0]
            image = f['filename']
            extn = os.path.splitext(image)[1]
            if extn in ('.jpg','.png','.bmp','.jpeg'):
                name =str(int(random.random()*10000000000000))
                fh = open(__UPLOADS__ + name + extn, 'wb')
                fh.write(f['body'])
                image = name+extn
                
    
            else:
                self.finish('this is is not image file')
        except:
            image = self.get_argument('image', None)
        if form.validate():
            form.image.data = image 
            print(form.image.data )  
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
            
            

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        u = User.query.get(self.get_cookie('user'))
        self.clear_all_cookies()
        
        self.render("login.html", user="")
        
  
    
        

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html", user="")
        
    def post(self):
       get_user(self)
      
            
class ProductsListHandler(BaseHandler):
    def get(self):
        q = Product.query.all()

        self.render("products_list.html", items= q )
        
        
    def post(self):
        cart(self)
        self.redirect('/products')
        
class CartHandler(tornado.web.RequestHandler):
    def get(self):
        q = Cart.query.all()
        self.render('cart.html', carts = q)


class ProfileHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie('user')
        q = Cart.query.filter_by(user_id = user_id).all()
        self.render('cart.html', carts = q)
        
class Qty(tornado.web.UIModule, tornado.web.RequestHandler):        
    def render(self):
        cart_id = self.get_cookie('cart_id' , None)
        i = []
        if cart_id:
            c = Cart.query.filter_by(id = cart_id).first()
            i = [x.qty for x in c.items]
        s = sum(i)
        return s