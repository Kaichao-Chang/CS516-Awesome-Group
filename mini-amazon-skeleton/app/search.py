from ast import keyword
from crypt import methods
from unicodedata import category
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
import datetime

from app.models.search import Search, Order_Search

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
from .models.seller import Seller
bp = Blueprint('search', __name__)

# class SearchForm(FlaskForm):
#     type = StringField('Type', validators=[DataRequired()])
#     search_message = StringField('search-message', validators=[DataRequired()])
#     submit = SubmitField('Search')


@bp.route("/search", methods=['GET', "POST"])
def search():
    if current_user.is_authenticated:
        if Seller.is_seller(current_user.id):
            current_user.is_current_seller = True    
    # form = SearchForm()
    # type = form.type.data
    # search_message = form.search_message.data

    cate = request.form.get('category')
    search_msg = request.form.get('search-message')
    order = int(request.form.get('order'))

    product = Search.search_product(search_msg, cate, order)

    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    return render_template('search_result.html', search_msg=search_msg, search_catagory=cate, orderby=order, match_products=product,
                           purchase_history=purchases,)

@bp.route("/search_order", methods=['GET', "POST"])
def search_order():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True    

    search_msg = request.form.get('search-message')
    fulfill = int(request.form.get('fulfill'))
    
    key_word = 0 
    if len(search_msg) == 0:
        key_word = 1
    
    search_order = Order_Search.search_order(current_user.id, search_msg, fulfill)

    return render_template('order_search_result.html', search_order = search_order, search_msg = search_msg, fulfill = fulfill, key_word = key_word)
