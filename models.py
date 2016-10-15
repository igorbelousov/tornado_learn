#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Boolean, Text, MetaData, ForeignKey, SmallInteger, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

basedir = os.path.abspath(os.path.dirname(__file__))
Base = declarative_base()
engine = create_engine('postgresql://postgres:UjhrB37@localhost/theshop', echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()


def init_db(engine):
  Base.metadata.create_all(bind=engine)

#models
ROLE_USER = 0
ROLE_ADMIN = 1

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    nickname = Column(String(64), index = True, unique = True)
    email = Column(String(120), index = True, unique = True)
    password = Column(String(), index = True, unique = True)
    role = Column(SmallInteger, default = ROLE_USER)
    
    def __init__(self, nickname, email, password, role):
        self.nickname = nickname
        self.email = email
        self.password = password        
        self.role = role        

    def __repr__(self):
        return self.nickname
      
      
# shop models
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    title = Column(String(255))
    slug = Column(String(255))
    active = Column(Boolean(), default = True)
    description = Column(String)
    seo_title = Column(String(255))
    seo_description = Column(String(255))
    seo_keywords = Column(String(140))

    def __init__(self, title,  slug, active, description='',  seo_description='',
                 seo_keywords='', seo_title='' ):
        self.title = title
        self.active = active
        self.slug = slug
        self.description = description
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.seo_title = seo_title
        
    def __repr__(self):
        return self.title    
        
class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key = True)
    title = Column(String(255))
    slug = Column(String(255))
    active = Column(Boolean(), default = True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", backref=backref('serie', order_by=id))
    description = Column(String)
    seo_title = Column(String(255))
    seo_description = Column(String(255))
    seo_keywords = Column(String(140))

    def __init__(self, title,  slug, active, category_id, description='',  seo_description='',
                 seo_keywords='', seo_title='' ):
        self.title = title
        self.active = active
        self.slug = slug
        self.category_id = category_id
        self.description = description
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.seo_title = seo_title
        
    def __repr__(self):
        return self.title    


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key = True)
    title = Column(String(255))
    slug = Column(String(255))
    active = Column(Boolean(), default = True)
    description = Column(String)
    image = Column(String)
    seo_title = Column(String(255))
    seo_description = Column(String(255))
    seo_keywords = Column(String(140))

    def __init__(self, title,  slug, active, image='', description='',  seo_description='',
                 seo_keywords='', seo_title='' ):
        self.title = title
        self.active = active
        self.image = image
        self.slug = slug
        self.description = description
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.seo_title = seo_title
    
    def __repr__(self):
        return self.title    

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key = True)
    title = Column(String(255))
    slug = Column(String(255))
    active = Column(Boolean(), default = True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", backref=backref('product', order_by=id))
    series_id = Column(Integer, ForeignKey('series.id'))
    series = relationship("Series", backref=backref('products', order_by=id))
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship("Brand", backref=backref('products', order_by=id))
    price = Column(Float)
    sale_price = Column(Float)
    scu = Column(String(30))
    description = Column(Text, info={'description': u'Содержание Статьи',  'label': u'Содержание'})
    image = Column(String)
    seo_title = Column(String(255))
    seo_description = Column(String(255))
    seo_keywords = Column(String(140))

    def __init__(self, title,  slug, active, category_id, series_id, brand_id, price='',
                 sale_price='', scu='',image='', description='',  seo_description='',
                 seo_keywords='', seo_title='' ):
        self.title = title
        self.active = active
        self.slug = slug
        self.category_id = category_id
        self.series_id = series_id
        self.brand_id = brand_id
        self.image = image
        self.price = price
        self.sale_price =sale_price
        self.scu = scu
        self.description = description
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.seo_title = seo_title

    def __repr__(self):
        return self.title
      
      
# cart model
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref('carts', order_by=id))
    
    def __init__(self, user_id):
        self.user_id = user_id
        
        

    def __repr__(self):
        return '<Cart ID %r>' % (self.id)
    
    
class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key = True)
    item_id = Column(Integer, ForeignKey('product.id'))
    cart_id = Column(Integer, ForeignKey('cart.id'))
    qty = Column(Integer)
    cart = relationship("Cart", backref=backref('items', order_by=id))
    item = relationship("Product", backref=backref('items', order_by=id))
    
    
    def __init__(self, item_id, cart_id, qty):
        self.item_id = item_id
        self.cart_id = cart_id
        self.qty = qty

        
        

    def __repr__(self):
        return '<OrderItem ID %r>' % (self.id)

      
#blog model
class PostCategory(Base):
    __tablename__ = 'postcategory'
    id = Column(Integer, primary_key = True)
    title = Column(String(255))
    slug = Column(String(255))
    description = Column(String)
    seo_title = Column(String(255))
    seo_description = Column(String(255))
    seo_keywords = Column(String(140))

    def __init__(self, title,  slug, description='',  seo_description='', seo_keywords='', seo_title='' ):
        self.title = title
        self.slug = slug
        self.description = description
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.seo_title = seo_title

    def __repr__(self):
        return self.title

class Article(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key = True)
    title = Column(String(255), info={'description': u'',  'label': u'Заголовок'})
    slug = Column(String(255), info={'description': u'Название в адресной строке',  'label': u'URL'})
    image = Column(String)
    category_id = Column(Integer, ForeignKey('postcategory.id'))
    category = relationship("PostCategory", backref=backref('article', order_by=id))
    content = Column(Text, info={'description': u'Содержание Статьи',  'label': u'Содержание'})
    description = Column(String)
    seo_title = Column(String(255))
    seo_description = Column(String(255))
    seo_keywords = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship("User", backref=backref('posts', order_by=id))

    def __init__(self, title,  slug, category_id, content, author_id, description='', image='',
                 seo_description='', seo_keywords='', seo_title='' ):
        self.title = title
        self.slug = slug
        self.category_id = category_id
        self.description = description
        self.content = content
        self.author_id = author_id
        self.image = image
        self.seo_description = seo_description
        self.seo_keywords = seo_keywords
        self.seo_title = seo_title

    def __repr__(self):
        return '<Post %r>' % (self.title)
    
def creat_user():
    n =input('please you name  ')
    e = input('please you email  ')
    p = input('please you password  ')
    u = User(nickname = n, email= e, password = p, role=1)
    db_session.add(u)
    db_session.commit()

#starter
if __name__ == "__main__":
    init_db(engine)
    creat_user()