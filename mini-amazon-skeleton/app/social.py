from flask import Blueprint, render_template, request
from flask_login import current_user

from .models.social import ProductReview, SellerReview

social_bp = Blueprint("social", __name__, url_prefix="/social/")


@social_bp.route("/product_review/<int:product_id>", methods=['GET', "POST"])
def product_reviews(product_id: int):
    if request.method == 'POST' and current_user.is_authenticated:
        review_type = request.form.get('review-type')
        if review_type == "new":
            user_id = current_user.id
            review_content = request.form.get('review-content')
            star = int(request.form.get('star'))
            ProductReview.insert_review(user_id, product_id, review_content, star)
        elif review_type == "update":
            user_id = current_user.id
            review_content = request.form.get('review-content')
            star = int(request.form.get('star'))
            ProductReview.update_review(user_id, product_id, review_content, star)
        elif review_type == "delete":
            user_id = current_user.id
            ProductReview.delete_review(user_id, product_id)
    reviews = ProductReview.get_reviews_of_one_product(product_id)
    return render_template("social/product_review.html", product_reviews=reviews)


@social_bp.route("/seller_review/<int:seller_id>", methods=['GET', "POST"])
def seller_reviews(seller_id: int):
    if request.method == 'POST' and current_user.is_authenticated:
        review_type = request.form.get('review-type')
        if review_type == "new":
            user_id = current_user.id
            review_content = request.form.get('review-content')
            star = int(request.form.get('star'))
            SellerReview.insert_review(user_id, seller_id, review_content, star)
        elif review_type == "update":
            user_id = current_user.id
            review_content = request.form.get('review-content')
            star = int(request.form.get('star'))
            SellerReview.update_review(user_id, seller_id, review_content, star)
        elif review_type == "delete":
            user_id = current_user.id
            SellerReview.delete_review(user_id, seller_id)

    reviews = SellerReview.get_reviews_of_one_seller(seller_id)
    return render_template("social/seller_review.html", seller_reviews=reviews)
