from crypt import methods
from flask import Blueprint, flash, redirect, render_template, request, url_for, request
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from flask import Blueprint
bp = Blueprint('search', __name__)

class SearchForm(FlaskForm):
    type = StringField('Type', validators=[DataRequired()])
    search_message = StringField('Search Message', validators=[DataRequired()])
    submit = SubmitField('Search')

@bp.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    type = form.type.data
    search_message = form.search_message.data

    print(type)
    print(search_message)

    return render_template('search_result.html', title='Result', form=form)
