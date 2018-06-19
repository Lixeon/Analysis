# -- coding: utf-8 --
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
from flask_babel import _, lazy_gettext as _l
class RequestForm(FlaskForm):
    companyname = StringField(_l('Your Company Name'), validators=[DataRequired()])
    username = StringField(_l('Your Name'), validators=[DataRequired()])
    email = StringField(_l('Email Address'), validators=[DataRequired(),Email()])
    message = TextAreaField(_l('Requests for our product'), validators=[DataRequired(),Length(max=200)])
    submit = SubmitField(_l('Submit'))