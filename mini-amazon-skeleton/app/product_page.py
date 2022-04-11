from flask import Blueprint, render_template
from .models.product_page import Product_page

bp = Blueprint('product_page', __name__)

@bp.route('/page/<int:product_id>')
def page(product_id:int):
    list, name = Product_page.get_product(product_id)
    return render_template("product_page.html", product_list = list, product_name = name)

