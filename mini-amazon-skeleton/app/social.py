from flask import Blueprint, render_template

from .models.social import Review

social_bp = Blueprint("social", __name__, url_prefix="/social/")


@social_bp.route("/review/<int:product_id>")
def product_reviews(product_id: int):
    # get all reviews for one product:
    reviews = Review.get_reviews_of_one_product(product_id)
    return render_template("social/review.html", product_reviews=reviews)
