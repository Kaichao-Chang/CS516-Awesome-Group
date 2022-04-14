from flask import Blueprint, render_template, request
from flask_login import current_user

from .models.social import ProductReview, SellerReview
from .models.seller import Seller
social_bp = Blueprint("social", __name__, url_prefix="/social/")


@social_bp.route("/product_reviews/<int:product_id>", methods=['GET', "POST"])
def product_reviews(product_id: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
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
        elif review_type == "upvote":
            user_id = current_user.id
            review_id = int(request.form.get('review-id'))
            ProductReview.upvote_review(review_id)
    reviews = ProductReview.get_reviews_of_one_product(product_id)
    return render_template("social/review.html", reviews=reviews, review_type="product_review")


@social_bp.route("/seller_reviews/<int:seller_id>", methods=['GET', "POST"])
def seller_reviews(seller_id: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
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
        elif review_type == "upvote":
            user_id = current_user.id
            review_id = int(request.form.get('review-id'))
            SellerReview.upvote_review(review_id)

    reviews = SellerReview.get_reviews_of_one_seller(seller_id)
    return render_template("social/review.html", reviews=reviews, review_type="seller_review")


@social_bp.route("/my_product_reviews")
def my_product_reviews():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    user_id = current_user.id
    reviews = ProductReview.get_reviews_of_one_user(user_id)
    return render_template("social/review.html", reviews=reviews, review_type="my_product_review")


@social_bp.route("/my_seller_reviews")
def my_seller_reviews():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    user_id = current_user.id
    reviews = SellerReview.get_reviews_of_one_user(user_id)
    return render_template("social/review.html", reviews=reviews, review_type="my_seller_review")
