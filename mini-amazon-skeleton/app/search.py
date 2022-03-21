from crypt import methods
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import datetime

from app.models.search import Search

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('search', __name__)

# class SearchForm(FlaskForm):
#     type = StringField('Type', validators=[DataRequired()])
#     search_message = StringField('Search Message', validators=[DataRequired()])
#     submit = SubmitField('Search')

@bp.route("/search", methods=['GET',"POST"])
def search():
    # form = SearchForm()
    # type = form.type.data
    # search_message = form.search_message.data
    
    # if type == 'products':
    #     print('searching for product')


    # # print(form)
    # # print('this is type')
    # # print(type)
    # print('this is search')
    # print(search_message)
    search_type = request.form.get('type')
    search_msg = request.form.get('Search Message')

    if search_type == 'products':
    #     print('searching for product', search_msg)

        product = Search.search_product(search_msg)



    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    return render_template('search_result.html', search_msg=search_msg, match_products=product,
                           purchase_history=purchases)
