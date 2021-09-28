# 在「一對多」中使用 lazy = select
# lazy = select 同等於 lazy = True 亦同等於默認值，可以不寫，但官方有提示 explicit is better than implicit.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lazy_select.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# There can be many students in a class.

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    students = db.relationship('Student', backref='_class', lazy="select") # <------- "lazy" is at here!

    def __repr__(self):
        return '<Class: %r>' %self.name

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    def __repr__(self):
        return '<Student: %r>' %self.name
    
# lazy defines when SQLAlchemy will load the data from the database:
# 'select' / True (which is the default, but explicit is better than implicit)
# 'joined' / False
# 'subquery' 
# 'dynamic'
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

# Create some classes and students.
# c1 = Class(name='English')
# c2 = Class(name='Math')
# c3 = Class(name='Spanish')
# db.session.add(c1)
# db.session.add(c2)
# db.session.add(c3)
# s1 = Student(name='Tom', class_id=1)
# s2 = Student(name='Ray', class_id=1)
# s3 = Student(name='Sam', class_id=2)
# db.session.add(s1)
# db.session.add(s2)
# db.session.add(s3)
# db.session.commit()

# If lazy = select, it directly returns the associated objects, and a list is composed of the objects as elements.
# 如果 lazy = select，是直接返回了關聯的對象，並由對象為元素組成了一個 list。

# >>> c1
# <Class: 'English'>

# >>> c1.students
# [<Student: 'Tom'>, <Student: 'Ray'>] <----- 由對象(Student)為元素組成了一個 list

# The attribute of the Class: backref='_class', make the class instantiation be able to use ._class  to access Class content.
# 通過 Class 裡面的 backref=_class 屬性，實體對象能夠使用 ._class 訪問 Class 的內容

# >>> s1
# <Student: 'Tom'>

# >>> s1._class
# <Class: 'English'>
