# 在「多對多」中使用 lazy = dynamic

# lazy="dynamic" can only be used in one-to-many and many-to-many relationships, not in one-to-one and many-to-one relationships.
# lazy="dynamic" 只可以用在一對多和多對多關係中，不可以用在一對一和多對一中。

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lazy_dynamic_many_to_many.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

registrations = db.Table('registrations',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
    )

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    students = db.relationship('Student', 
        secondary = registrations, 
        backref = db.backref('_class',lazy="dynamic"), 
        lazy = "dynamic"
        ) # <------- "lazy" is at here!

    def __repr__(self):
        return '<Class: %r>' %self.name

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

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
# s1 = Student(name='Tom')
# s2 = Student(name='Ray')
# s3 = Student(name='Sam')
# db.session.add(s1)
# db.session.add(s2)
# db.session.add(s3)
# db.session.commit()
# Make some relationship between classes and students
# 因為在 class Class(db.Model): 裡面的 backref = db.backref('_class',lazy="dynamic")
# 可以看到設定好的 '_class'
# 所以可以用 ._class 將學生和課程做連結
# s1._class.append(c1)
# s1._class.append(c2)
# s2._class.append(c1)
# s2._class.append(c3)
# s3._class.append(c2)
# s3._class.append(c3)
# db.session.commit()

# 在檔案 lazy_select.py 中得知：
# 如果 lazy = select
# >>> c1.students
# [<Student: 'Tom'>, <Student: 'Ray'>]
# 由對象(Student)為元素組成了一個 list

# 在檔案 lazy_dynamic_one_to_many.py 中得知：
# 如果 lazy = dynamic
# >>> c1.students
# <sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x7fdb500434f0>
# 變成了一個查詢對象，而不是直接生成列表。

# 目前檔案為 lazy_dynamic_many_to_many.py
# 當前的 lazy = dynamic
# >>> c1.students
# <sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x7ff83120a550>
# 一樣是一個查詢對象，不是直接生成列表。

# >>> c1
# <Class: 'English'>

# >>> c1.students
# <sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x7fdb500434f0>

# >>> c1.students.all()
# [<Student: 'Tom'>, <Student: 'Ray'>]

# >>> c1.students.filter_by(id=1).first()
# <Student: 'Tom'>

# 通過 Class 裡面的 backref=_class 屬性，實體對象能夠使用 ._class 訪問 Class 的內容

# >>> s1
# <Student: 'Tom'>

# >>> s1._class
# <sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x7ff8000301f0>

# >>> s1._class.all()
# [<Class: 'Math'>, <Class: 'English'>]
