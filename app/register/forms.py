# --coding:utf-8--

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], label=u'用户名')
    password = PasswordField(validators=[DataRequired()], label=u'密码')
    submit = SubmitField(label=u'提交')