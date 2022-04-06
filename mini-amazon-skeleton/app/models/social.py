from flask import current_app as app


class ProductReview:
    def __init__(
            self, user_id: int, user_name: str, product_id: int, content: str, star: int,
            created_at: str):
        self.user_id = user_id
        self.user_name = user_name
        self.product_id = product_id
        self.content = content
        self.star = star
        self.created_at = created_at.strftime("%I:%M:%S%p<br/>%B/%d/%Y")

    @staticmethod
    def get_reviews_of_one_product(product_id: int):
        rows = app.db.execute(
            "SELECT uid, CONCAT(firstname, ' ', lastname) AS user_name, pid, content, star, created_at "
            "FROM ProductReviews "
            "LEFT JOIN Users ON ProductReviews.uid = Users.id "
            "WHERE ProductReviews.pid = :product_id "
            "ORDER BY created_at DESC", product_id=product_id,)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def insert_review(user_id: int,
                      product_id: int,
                      content: str,
                      star: int):
        # Insert
        app.db.execute(
            "INSERT INTO ProductReviews (uid, pid, content, star) "
            "VALUES(:uid, :pid, :content, :star) ",
            uid=user_id,
            pid=product_id,
            content=content,
            star=star
        )
        ProductReview.update_product_score(product_id)

    @staticmethod
    def update_review(user_id: int,
                      product_id: int,
                      content: str,
                      star: int):
        app.db.execute(
            "UPDATE ProductReviews "
            "SET content = :content, star = :star "
            "WHERE uid = :uid AND pid = :pid ",
            uid=user_id,
            pid=product_id,
            content=content,
            star=star
        )
        ProductReview.update_product_score(product_id)

    @staticmethod
    def delete_review(user_id: int,
                      product_id: int):
        app.db.execute(
            "DELETE FROM ProductReviews "
            "WHERE uid = :uid AND pid = :pid ",
            uid=user_id,
            pid=product_id
        )
        ProductReview.update_product_score(product_id)

    @staticmethod
    def update_product_score(product_id: int):
        # Update average score
        app.db.execute(
            "WITH TempTable(avg_star) AS "
            "(SELECT AVG(star) from ProductReviews "
            "WHERE pid = :pid) "
            "   UPDATE Products "
            "   SET overall_star = TempTable.avg_star "
            "   FROM TempTable "
            "   WHERE id = :pid;",
            pid=product_id
        )


class SellerReview:
    def __init__(
            self, user_id: int, user_name: str, seller_id: int, content: str, star: int,
            created_at: str):
        self.user_id = user_id
        self.user_name = user_name
        self.product_id = seller_id
        self.content = content
        self.star = star
        self.created_at = created_at.strftime("%I:%M:%S%p<br/>%B/%d/%Y")

    @staticmethod
    def get_reviews_of_one_seller(seller_id: int):
        rows = app.db.execute(
            "SELECT customer_id, CONCAT(firstname, ' ', lastname) AS user_name, seller_id, content, star, created_at "
            "FROM SellerReviews "
            "LEFT JOIN Users ON SellerReviews.customer_id = Users.id "
            "WHERE SellerReviews.seller_id = :seller_id "
            "ORDER BY created_at DESC", seller_id=seller_id)
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def insert_review(user_id: int,
                      seller_id: int,
                      content: str,
                      star: int):
        app.db.execute(
            "INSERT INTO SellerReviews (customer_id, seller_id, content, star) "
            "VALUES(:uid, :sid, :content, :star) ",
            uid=user_id,
            sid=seller_id,
            content=content,
            star=star
        )
        SellerReview.update_seller_score(seller_id)

    @staticmethod
    def update_review(user_id: int,
                      seller_id: int,
                      content: str,
                      star: int):
        app.db.execute(
            "UPDATE SellerReviews "
            "SET content = :content, star = :star "
            "WHERE customer_id = :uid AND seller_id = :sid ",
            uid=user_id,
            sid=seller_id,
            content=content,
            star=star
        )
        SellerReview.update_seller_score(seller_id)

    @staticmethod
    def delete_review(user_id: int,
                      seller_id: int):
        app.db.execute(
            "DELETE FROM SellerReviews "
            "WHERE customer_id = :uid AND seller_id = :sid ",
            uid=user_id,
            sid=seller_id
        )
        SellerReview.update_seller_score(seller_id)

    @staticmethod
    def update_seller_score(seller_id: int):
        # Update average score
        app.db.execute(
            "WITH TempTable(avg_star) AS "
            "(SELECT AVG(star) from SellerReviews "
            "WHERE seller_id = :sid) "
            "   UPDATE Sellers "
            "   SET overall_star = TempTable.avg_star "
            "   FROM TempTable "
            "   WHERE id = :sid;",
            sid=seller_id
        )
