from exts import db
from wtforms import Form, TextField, PasswordField
from wtforms.validators import Required


class CC(db.Model):
    __tablename__ = 'cc'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class LoginForm(Form):
    username = TextField('name', [Required()])
    password = PasswordField('password', [Required()])


class Student(db.Model):
    __tablename__ = 'student'
    bf_StudentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bf_Name = db.Column(db.String(20), nullable=False)
    bf_sex = db.Column(db.String(10), nullable=False)
    bf_nation = db.Column(db.String(20), nullable=False)
    bf_BornDate = db.Column(db.String(255), nullable=False)
    cla_Name = db.Column(db.String(40), nullable=False)
    bf_NativePlace = db.Column(db.String(255), nullable=False)
    bf_ResidenceType = db.Column(db.String(255), nullable=False)
    bf_policy = db.Column(db.String(50), nullable=False)
    cla_id = db.Column(db.Integer, nullable=False)
    cla_term = db.Column(db.String(255), nullable=False)
    bf_zhusu = db.Column(db.String(5), nullable=False)
    bf_leaveSchool = db.Column(db.String(5), nullable=False)
    bf_qinshihao = db.Column(db.String(20), nullable=False)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


