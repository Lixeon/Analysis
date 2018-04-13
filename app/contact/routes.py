from flask import render_template, redirect, url_for, flash, request
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from app.contact import bp
from app.contact.forms import RequestForm

@bp.route('/', methods=['GET', 'POST'])
def  index():
    form = RequestForm()
    if form.validate_on_submit():
        return render_template('contact/success.html', title=_('Success'),contact='active')
    return render_template('contact/index.html', title=_('Contact'),form=form,contact='active') 

