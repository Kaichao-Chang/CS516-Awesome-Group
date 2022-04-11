from flask import current_app as app


class Product:
    def __init__(self,
                 id,
                 name,
                 price,
                 available,
                 seller_id,
                 seller_name: str,
                 product_overall_star: float,
                 inv: int,
                 n_seller_reviews: int,
                 seller_overall_star: float,
                 n_product_reviews: int):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.product_overall_star = round(product_overall_star, 1)
        self.inv = inv
        self.n_seller_reviews = n_seller_reviews
        self.seller_overall_star = round(seller_overall_star, 1)
        self.n_product_reviews = n_product_reviews

    @staticmethod
    def get_all(available=True):
        product_info = app.db.execute(
            "SELECT Products.id, name, price, available, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, overall_star, inv "
            "FROM Products "
            "LEFT JOIN Users ON Products.seller_id = Users.id "
            "WHERE available = :available "
            "ORDER BY Products.id DESC", available=available)

        seller_review_info = app.db.execute(
            "SELECT COUNT(SellerReviews.id), COALESCE(AVG(SellerReviews.star), 0) "
            "FROM Products "
            "LEFT JOIN SellerReviews ON SellerReviews.seller_id = Products.seller_id "
            "WHERE available = :available "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC", available=available)

        product_review_info = app.db.execute(
            "SELECT COUNT(ProductReviews.id)"
            "FROM Products "
            "LEFT JOIN ProductReviews ON ProductReviews.pid = Products.id "
            "WHERE available = :available "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC", available=available)

        return [Product(*product_info[i], *seller_review_info[i], *product_review_info[i]) for i in range(len(product_info))]

    @staticmethod
    def post_item(name, price, uid, number):
        app.db.execute(
            "INSERT INTO Products(name, price, available, seller_id, inv)"
            "VALUES(:name, :price, TRUE, :uid, :number)"
            "RETURNING id",
            name=name,
            price=price,
            uid=uid,
            number=number)

    @staticmethod
    def get_all_by_seller(uid):
        product_info = app.db.execute(
            "SELECT Products.id, name, price, available, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, overall_star, inv "
            "FROM Products "
            "LEFT JOIN Users ON Products.seller_id = Users.id "
            "WHERE seller_id = :seller_id "
            "ORDER BY Products.id DESC", seller_id = uid)

        seller_review_info = app.db.execute(
            "SELECT COUNT(SellerReviews.id), COALESCE(AVG(SellerReviews.star), 0) "
            "FROM Products "
            "LEFT JOIN SellerReviews ON SellerReviews.seller_id = Products.seller_id "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC")

        product_review_info = app.db.execute(
            "SELECT COUNT(ProductReviews.id)"
            "FROM Products "
            "LEFT JOIN ProductReviews ON ProductReviews.pid = Products.id "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC")

        return [Product(*product_info[i], *seller_review_info[i], *product_review_info[i]) for i in range(len(product_info))]

    @staticmethod
    def items_on_sale(uid):
        product_info = app.db.execute(
            "SELECT Products.id, name, price, available, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, overall_star, inv "
            "FROM Products "
            "LEFT JOIN Users ON Products.seller_id = Users.id "
            "WHERE seller_id = :seller_id "
            "AND inv > 0"
            "ORDER BY Products.id DESC", seller_id = uid)

        seller_review_info = app.db.execute(
            "SELECT COUNT(SellerReviews.id), COALESCE(AVG(SellerReviews.star), 0) "
            "FROM Products "
            "LEFT JOIN SellerReviews ON SellerReviews.seller_id = Products.seller_id "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC")

        product_review_info = app.db.execute(
            "SELECT COUNT(ProductReviews.id)"
            "FROM Products "
            "LEFT JOIN ProductReviews ON ProductReviews.pid = Products.id "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC")

        return [Product(*product_info[i], *seller_review_info[i], *product_review_info[i]) for i in range(len(product_info))]

    @staticmethod
    def all_selling_items(uid):
        product_info = app.db.execute(
            "SELECT Products.id, name, price, available, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, overall_star, inv "
            "FROM Products "
            "LEFT JOIN Users ON Products.seller_id = Users.id "
            "WHERE seller_id = :seller_id "
            "ORDER BY Products.id DESC", seller_id = uid)

        seller_review_info = app.db.execute(
            "SELECT COUNT(SellerReviews.id), COALESCE(AVG(SellerReviews.star), 0) "
            "FROM Products "
            "LEFT JOIN SellerReviews ON SellerReviews.seller_id = Products.seller_id "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC")

        product_review_info = app.db.execute(
            "SELECT COUNT(ProductReviews.id)"
            "FROM Products "
            "LEFT JOIN ProductReviews ON ProductReviews.pid = Products.id "
            "GROUP BY Products.id "
            "ORDER BY Products.id DESC")

        return [Product(*product_info[i], *seller_review_info[i], *product_review_info[i]) for i in range(len(product_info))]

    @staticmethod
    def change_inv(id, inv):
        app.db.execute(
            "UPDATE Products "
            "SET inv = :inv "
            "WHERE id = :id",
        id = id,
        inv = inv
        )

    @staticmethod
    def product_remove(id):
        app.db.execute(
            "DELETE FROM Products "
            "WHERE id = :id ",
        id = id
        )
