from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available, seller_id, seller_name):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.seller_name = seller_name

    @staticmethod
    def get(id):
        rows = app.db.execute(
            "SELECT id, name, price, available, seller_id "
            "FROM Products "
            "WHERE id = :id",
            id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute(
            "SELECT id, name, price, available, uid "
            "FROM Products "
            "WHERE available = :available ",
            available=available)

        seller_ids = tuple([row[-1] for row in rows])
        seller_names = app.db.execute(
            "SELECT firstname, lastname "
            "FROM Users "
            "WHERE id IN :seller_ids",
            seller_ids=seller_ids
        )

        args_list = []
        for row, seller_name in zip(rows, seller_names):
            row = list(row)
            seller_name = list(seller_name)
            row.append(" ".join(seller_name))
            args_list.append(row)

        return [Product(*args) for args in args_list]

    @staticmethod
    def post_item(name, price, uid):
        app.db.execute(
            "INSERT INTO Products(name, price, available, uid)"
            "VALUES(:name, :price, TRUE, :uid) "
            "RETURNING id",
            name=name,
            price=price,
            uid = uid)
