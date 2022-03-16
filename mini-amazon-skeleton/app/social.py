from flask import Blueprint, render_template

from .models.social import ProductReview, SellerReview

social_bp = Blueprint("social", __name__, url_prefix="/social/")


@social_bp.route("/product_review/<int:product_id>")
def product_reviews(product_id: int):
    # get all reviews for one product:
    reviews = ProductReview.get_reviews_of_one_product(product_id)
    return render_template("social/product_review.html", product_reviews=reviews)


@social_bp.route("/seller_review/<int:seller_id>")
def seller_reviews(seller_id: int):
    # get all reviews for one seller:
    reviews = SellerReview.get_reviews_of_one_seller(seller_id)
    return render_template("social/seller_review.html", seller_reviews=reviews)
