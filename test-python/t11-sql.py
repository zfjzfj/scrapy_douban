# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


# 创建对象的基类:
Base = declarative_base()

## 定义User对象:
#class User(Base):
#    # 表的名字:
#    __tablename__ = 'user'
#
#    # 表的结构:
#    id = Column(String(20), primary_key=True)
#    name = Column(String(20))
#
#    def __repr__(self):
#	return "<User(name='%s')>" % ( self.name)

class User(Base):
    __tablename__ = 'user'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # 一对多:
    books = relationship('Book')

class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20), ForeignKey('user.id'))




# 初始化数据库连接:
engine = create_engine('mysql://root:root123@127.0.0.1:3306/test?charset=utf8',encoding='utf-8',echo=True)



Base.metadata.create_all(engine)


# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
new_book = Book(id='5', name='python',user_id='5')
# 添加到session:
session.add(new_book)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()


# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()
# 打印类型和对象的name属性:
print 'type:', type(user)
print  user
print user.id,user.name

# 关闭Session:
session.close()
