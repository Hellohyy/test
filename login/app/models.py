from exts import db
from . import Login_manager
from wtforms import Form, TextField, PasswordField
from wtforms.validators import Required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_login import UserMixin

# class LoginForm(Form):
#     username = TextField('name', [Required()])
#     password = PasswordField('password', [Required()])


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))