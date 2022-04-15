from flask import Blueprint, render_template
from flask_login import current_user
from .models.product_page import Product_page
from .models.seller import Seller

bp = Blueprint('product_page', __name__)

@bp.route('/page/<int:product_id>')
def page(product_id:int):
    if current_user.is_authenticated and Seller.is_seller(current_user.id):
        current_user.is_current_seller = True 
    list, name = Product_page.get_product(product_id)
    return render_template("product_page.html", product_list = list, product_name = name)

