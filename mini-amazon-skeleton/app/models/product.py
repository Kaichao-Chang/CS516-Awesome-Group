from email import charset
from flask import current_app as app
# TO DO:
# check file name duplicate

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

    # @deprecated
    # @staticmethod
    # def post_item(name, price, uid, number):
    #     app.db.execute(
    #         "INSERT INTO Products(name, price, available, seller_id, inv)"
    #         "VALUES(:name, :price, TRUE, :uid, :number)"
    #         "RETURNING id",
    #         name=name,
    #         price=price,
    #         uid=uid,
    #         number=number)

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

    # @deprecated
    # @staticmethod
    # def items_on_sale(uid):
    #     product_info = app.db.execute(
    #         "SELECT Products.id, name, price, available, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, overall_star, inv "
    #         "FROM Products "
    #         "LEFT JOIN Users ON Products.seller_id = Users.id "
    #         "WHERE seller_id = :seller_id "
    #         "AND available = true "
    #         "ORDER BY Products.id DESC", seller_id = uid)

    #     seller_review_info = app.db.execute(
    #         "SELECT COUNT(SellerReviews.id), COALESCE(AVG(SellerReviews.star), 0) "
    #         "FROM Products "
    #         "LEFT JOIN SellerReviews ON SellerReviews.seller_id = Products.seller_id "
    #         "GROUP BY Products.id "
    #         "ORDER BY Products.id DESC")

    #     product_review_info = app.db.execute(
    #         "SELECT COUNT(ProductReviews.id)"
    #         "FROM Products "
    #         "LEFT JOIN ProductReviews ON ProductReviews.pid = Products.id "
    #         "GROUP BY Products.id "
    #         "ORDER BY Products.id DESC")

    #     return [Product(*product_info[i], *seller_review_info[i], *product_review_info[i]) for i in range(len(product_info))]

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
            "UPDATE Products "
            "SET inv = 0 "
            "WHERE id = :id",
        id = id
        )
        app.db.execute(
            "UPDATE Products "
            "SET available = false "
            "WHERE id = :id",
        id = id
        )

    @staticmethod
    def selling_items_history(uid):
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


class Product2:
    def __init__(self,
                 id,
                 name,
                 price,
                 available,
                 seller_id,
                 seller_name: str,
                 product_overall_star: float,
                 inv: int,
                 cate: str,
                 descr: str,
                 img: str,
                 n_seller_reviews: int,
                 seller_overall_star: float,
                 n_product_reviews: int
                 ):
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
        self.cate = cate
        self.descr = descr
        self.img = img


    @staticmethod
    def post_item(name, price, cate, descr, img, uid, number):
        app.db.execute(
            "INSERT INTO Products(name, price,cate, descr, img, available, seller_id, inv)"
            "VALUES(:name, :price, :cate, :descr, :img, TRUE, :uid, :number)"
            "RETURNING id",
            name=name,
            price=price,
            cate=cate,
            descr=descr,
            img=img,
            uid=uid,
            number=number)

    @staticmethod
    def items_on_sale(uid):
        product_info = app.db.execute(
            "SELECT Products.id, name, price, available, seller_id, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name, overall_star, inv, cate, descr, img "
            "FROM Products "
            "LEFT JOIN Users ON Products.seller_id = Users.id "
            "WHERE seller_id = :seller_id "
            "AND available = true "
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
        print(product_info)
        return [Product2(*product_info[i], *seller_review_info[i], *product_review_info[i]) for i in range(len(product_info))]

    @staticmethod
    def change_name(id, name):
        app.db.execute(
            "UPDATE Products "
            "SET name = :name "
            "WHERE id = :id",
        id = id,
        name = name
        )

    @staticmethod
    def change_descr(id, descr):
        app.db.execute(
            "UPDATE Products "
            "SET descr = :descr "
            "WHERE id = :id",
        id = id,
        descr = descr
        )

    @staticmethod
    def change_cate(id, cate):
        app.db.execute(
            "UPDATE Products "
            "SET cate = :cate "
            "WHERE id = :id",
        id = id,
        cate = cate
        )

    @staticmethod
    def change_price(id, price):
        app.db.execute(
            "UPDATE Products "
            "SET price = :price "
            "WHERE id = :id",
        id = id,
        price = price
        )

    @staticmethod
    def change_img(id, img):
        app.db.execute(
            "UPDATE Products "
            "SET img = :img "
            "WHERE id = :id",
        id = id,
        img = img
        )
        