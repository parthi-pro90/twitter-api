from flask import flash, Blueprint, redirect, request, render_template, url_for
from .forms import LoginForm
from app import app
from app.login.controller import process_user_details

login_blueprint = Blueprint(
    'login_blueprint',
    __name__, 
    url_prefix='/user',
    template_folder='templates'
)

""" POST method, Form param (username)"""
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            detail = process_user_details(request.form['username'])
            if detail['status'] == 1:
                return redirect(url_for('timeline_blueprint.timeline', id=detail['id']))
            else:
                error = detail['message']

    flash(error)     
    return render_template('login.html', form=form, error=error)

# @login_blueprint.route('/home', methods=['GET', 'POST'])
# def home():
#     detail = process_user_details('na')
#     print(detail)
#     return detail  