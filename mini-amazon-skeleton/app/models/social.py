from flask import current_app as app


class ProductReview:
    def __init__(self, user_id: int, user_name: str, product_id: int, content: str):
        self.user_id = user_id
        self.user_name = user_name
        self.product_id = product_id
        self.content = content

    @staticmethod
    def get_reviews_of_one_product(product_id: int):
        rows = app.db.execute(
            "SELECT uid, CONCAT(firstname, ' ', lastname) AS user_name, pid, content "
            "FROM ProductReviews "
            "LEFT JOIN Users ON ProductReviews.uid = Users.id "
            "WHERE ProductReviews.pid = :product_id ",
            product_id=product_id,
        )
        return [ProductReview(*row) for row in rows]


class SellerReview:
    def __init__(self, user_id: int, user_name: str, seller_id: int, content: str):
        self.user_id = user_id
        self.user_name = user_name
        self.product_id = seller_id
        self.content = content

    @staticmethod
    def get_reviews_of_one_seller(seller_id: int):
        rows = app.db.execute(
            "SELECT customer_id, CONCAT(firstname, ' ', lastname) AS user_name, seller_id, content "
            "FROM SellerReviews "
            "LEFT JOIN Users ON SellerReviews.customer_id = Users.id "
            "WHERE SellerReviews.seller_id = :seller_id",
            seller_id=seller_id
        )
        return [SellerReview(*row) for row in rows]
