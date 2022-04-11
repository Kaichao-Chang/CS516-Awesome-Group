from flask import current_app as app


def order_reviews(reviews_ord_by_time):
    top_3_reviews = []
    for review in reviews_ord_by_time:
        if len(top_3_reviews) < 3:
            top_3_reviews.append(review)
            top_3_reviews.sort(key=lambda review: review.upvote, reverse=True)
            continue
        if review.upvote > top_3_reviews[-1].upvote:
            top_3_reviews.pop(-1)
            top_3_reviews.append(review)
            top_3_reviews.sort(key=lambda review: review.upvote, reverse=True)

    for review in top_3_reviews:
        reviews_ord_by_time.remove(review)
    top_3_reviews.extend(reviews_ord_by_time)
    ordered_reviews = top_3_reviews

    return ordered_reviews


class ProductReview:
    def __init__(self, review_id: int, user_id: int, user_name: str, product_id: int,
                 product_name: str, content: str, star: int, upvote: int, created_at: str):
        self.review_id = review_id
        self.user_id = user_id
        self.user_name = user_name
        self.product_id = product_id
        self.product_name = product_name
        self.content = content
        self.star = star
        self.upvote = upvote
        self.created_at = created_at.strftime("%I:%M:%S%p<br/>%B/%d/%Y")

    @staticmethod
    def get_reviews_of_one_product(product_id: int):
        rows = app.db.execute(
            "SELECT ProductReviews.id, uid, CONCAT(firstname, ' ', lastname) AS user_name, pid, ' ', content, star, upvote, created_at "
            "FROM ProductReviews "
            "LEFT JOIN Users ON ProductReviews.uid = Users.id "
            "WHERE ProductReviews.pid = :product_id "
            "ORDER BY created_at DESC", product_id=product_id)

        return order_reviews([ProductReview(*row) for row in rows])

    @staticmethod
    def get_reviews_of_one_user(user_id: int):
        rows = app.db.execute(
            "SELECT ProductReviews.id, uid, CONCAT(firstname, ' ', lastname) AS user_name, pid, name, content, star, upvote, created_at "
            "FROM ProductReviews "
            "LEFT JOIN Users ON ProductReviews.uid = Users.id "
            "LEFT JOIN Products ON ProductReviews.pid = Products.id "
            "WHERE ProductReviews.uid = :user_id "
            "ORDER BY created_at DESC", user_id=user_id)
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

    @staticmethod
    def upvote_review(review_id: int):
        app.db.execute(
            "UPDATE ProductReviews "
            "SET upvote = upvote + 1 "
            "WHERE id = :rid ",
            rid=review_id
        )


class SellerReview:
    def __init__(
            self, review_id: int, user_id: int, user_name: str, seller_id: int, seller_name: str,
            content: str, star: int, upvote: int, created_at: str):
        self.review_id = review_id
        self.user_id = user_id
        self.user_name = user_name
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.content = content
        self.star = star
        self.upvote = upvote
        self.created_at = created_at.strftime("%I:%M:%S%p<br/>%B/%d/%Y")

    @staticmethod
    def get_reviews_of_one_seller(seller_id: int):
        rows = app.db.execute(
            "SELECT SellerReviews.id, customer_id, CONCAT(firstname, ' ', lastname) AS user_name, seller_id, ' ', content, star, upvote, created_at "
            "FROM SellerReviews "
            "LEFT JOIN Users ON SellerReviews.customer_id = Users.id "
            "WHERE SellerReviews.seller_id = :seller_id "
            "ORDER BY created_at DESC", seller_id=seller_id)
        return order_reviews([SellerReview(*row) for row in rows])

    @staticmethod
    def get_reviews_of_one_user(user_id: int):
        rows = app.db.execute(
            "WITH SRUser(rid, customer_id, user_name, seller_id, content, star, upvote, created_at) AS "
            "(SELECT SellerReviews.id, customer_id, CONCAT(Users.firstname, ' ', Users.lastname) AS user_name, seller_id, content, star, upvote, created_at "
            "FROM SellerReviews "
            "LEFT JOIN Users ON SellerReviews.customer_id = Users.id "
            "WHERE SellerReviews.customer_id = :user_id) "
            "    SELECT rid, customer_id, user_name, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, content, star, upvote, created_at "
            "    FROM SRUser "
            "    LEFT JOIN Users ON SRUser.seller_id = Users.id  "
            "    ORDER BY created_at DESC", user_id=user_id)
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
    def update_seller_score(seller_id: int):
        # Update average score
        app.db.execute(
            "WITH TempTable(avg_star) AS "
            "(SELECT AVG(star) from SellerReviews "
            "WHERE seller_id = :sid) "
            "   UPDATE Sellers "
            "   SET overall_star = TempTable.avg_star "
            "   FROM TempTable "
            "   WHERE id = :sid ",
            sid=seller_id
        )

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
    def upvote_review(review_id: int):
        app.db.execute(
            "UPDATE SellerReviews "
            "SET upvote = upvote + 1 "
            "WHERE id = :rid ",
            rid=review_id
        )
