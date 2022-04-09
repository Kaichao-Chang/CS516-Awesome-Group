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
            "SELECT COUNT(SellerReviews.id), overall_star "
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
        sells = app.db.execute(
            "SELECT id, name, price, available, seller_id, overall_star, ingv "
            "FROM Products "
            "WHERE seller_id = :uid",
            uid=uid)

        seller_ids = tuple([sell[-3] for sell in sells])

        seller_names = app.db.execute(
            "SELECT firstname, lastname "
            "FROM Users "
            "WHERE id IN :seller_ids",
            seller_ids=seller_ids
        )

        a_list = []
        for row, seller_name in zip(sells, seller_names):
            row = list(row)
            seller_name = list(seller_name)
            row.append(" ".join(seller_name))
            a_list.append(row)

        return Product(*(a_list[0])) if a_list is not None else None
