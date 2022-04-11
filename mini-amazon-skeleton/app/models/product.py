from curses import A_LEFT
from flask import current_app as app


class Product:
    def __init__(self,
                 id,
                 name,
                 price,
                 available,
                 seller_id,
                 overall_star: float,
                 inv,
                 seller_name: str):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.overall_star = round(overall_star)
        self.inv = inv

    @staticmethod
    def get(id):
        rows = app.db.execute(
            "SELECT id, name, price, available, seller_id, overall_star "
            "FROM Products "
            "WHERE id = :id",
            id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute(
            "SELECT id, name, price, available, seller_id, overall_star, inv "
            "FROM Products "
            "WHERE available = :available ",
            available=available)
        print(rows)
        seller_ids = tuple([row[-3] for row in rows])
        
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
    def post_item(name, price, uid, number):
        app.db.execute(
            "INSERT INTO Products(name, price, available, seller_id, inv)"
            "VALUES(:name, :price, TRUE, :uid, :number)"
            "RETURNING id",
            name=name,
            price=price,
            uid=uid,
            number = number)
    
    @staticmethod
    def get_all_by_seller(seller_id):
        rows = app.db.execute(
            "SELECT id, name, price, available, seller_id, overall_star, inv "
            "FROM Products "
            "WHERE seller_id = :seller_id ",
            seller_id = seller_id)
        seller_ids = tuple([row[-3] for row in rows])
        
        seller_names = app.db.execute(
            "SELECT firstname, lastname "
            "FROM Users "
            "WHERE id IN :seller_ids",
            seller_ids=seller_ids
        )
        
        seller_name = [('a')]

        args_list = []
        for row in zip(rows):
            row = list(row[0])
            row.append(seller_name[0])
            row = tuple(row)
            args_list.append(row)
        
        print(args_list)
        return [Product(*args) for args in args_list]
