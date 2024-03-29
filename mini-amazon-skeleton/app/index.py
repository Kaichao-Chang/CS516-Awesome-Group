import datetime

from flask import Blueprint, render_template
from flask_login import current_user

from .models.product import Product
from .models.purchase import Purchase
from .models.seller import Seller

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    if current_user.is_authenticated:
        if Seller.is_seller(current_user.id):
            current_user.is_current_seller = True
    

     # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            # Need to check the following line: 
            current_user.id, datetime.datetime(1980, 9, 3, 0, 0, 0), datetime.datetime(2023, 9, 4, 1, 2, 1), 'a', 'a')

        if Seller.is_seller(current_user.id):
            current_user.is_current_seller = True
    else:
        purchases = None
    #purchases = []


    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase=purchases)
