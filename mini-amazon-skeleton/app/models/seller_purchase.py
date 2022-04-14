from flask import current_app as app


class Seller_purchase:
    def __init__(self, id, uid, buyer_fname, buyer_lname, buyer_addr, pid, seller_id, quantity, fulfilled_by_seller, time_purchased, p_name, price, time_fulfilled):
        self.id = id
        self.uid = uid
        self.buyer_fname = buyer_fname
        self.buyer_lname = buyer_lname
        self.buyer_addr = buyer_addr
        self.pid = pid
        self.seller_id = seller_id
        self.quantity = quantity
        self.fulfilled_by_seller = fulfilled_by_seller
        self.time_purchased = time_purchased
        self.p_name = p_name
        self.price = price 
        self.time_fulfilled = time_fulfilled

    @staticmethod
    def get_all_by_seller(uid):
        rows = app.db.execute(
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled "
            "From Purchases "
            "LEFT JOIN Users  "
            "ON Purchases.uid = Users.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Order_fulfill "
            "ON Purchases.id = Order_fulfill.id "
            "WHERE Purchases.seller_id = :uid "
            "ORDER BY time_purchased DESC",
                              uid=uid)
        return [Seller_purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_purchaseid(uid, purchases_id):
        rows = app.db.execute(
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled "
            "From Purchases "
            "LEFT JOIN Users  "
            "ON Purchases.uid = Users.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Order_fulfill "
            "ON Purchases.id = Order_fulfill.id "
            "WHERE Purchases.seller_id = :uid "
            "AND Purchases.id = :purchases_id "
            "ORDER BY time_purchased DESC",
                              uid=uid,
                              purchases_id = purchases_id)
        print(rows)
        return [Seller_purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_product(pid, uid):
        rows = app.db.execute(
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled "
            "From Purchases "
            "LEFT JOIN Users  "
            "ON Purchases.uid = Users.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Order_fulfill "
            "ON Purchases.id = Order_fulfill.id "
            "WHERE Purchases.seller_id = :uid "
            "AND Products.id = :pid "
            "ORDER BY time_purchased DESC",
                              uid=uid,
                              pid = pid)
        print(rows)
        return [Seller_purchase(*row) for row in rows]

    @staticmethod
    def get_product_name(pid):
        p_name = app.db.execute(
            "SELECT name "
            "FROM Products "
            "WHERE id = :pid",
            pid = pid)
        
        return p_name

    @staticmethod
    def order_fulfill(id):
        app.db.execute(
            "UPDATE purchases "
            "SET fulfill_by_seller = true "
            "WHERE id = :id",
            id = id 
        )

        app.db.execute(
            "INSERT INTO order_fulfill(id, time_fulfilled) "
            "VALUES (:id, now()::timestamp)",
            id = id)
        
        product_id = app.db.execute(
            "SELECT pid "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        product_id = product_id[0][0]

        quantity = app.db.execute(
            "SELECT quantity "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        inv = app.db.execute(
            "SELECT inv "
            "FROM Products "
            "WHERE id = :product_id",
            product_id = product_id
        )

        new_inv = inv[0][0] - quantity[0][0]

        app.db.execute(
            "UPDATE Products "
            "SET inv = :new_inv "
            "WHERE id = :product_id",
            product_id = product_id,
            new_inv = new_inv
        )

    @staticmethod
    def enough_inv(id):
        
        product_id = app.db.execute(
            "SELECT pid "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        product_id = product_id[0][0]

        quantity = app.db.execute(
            "SELECT quantity "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        inv = app.db.execute(
            "SELECT inv "
            "FROM Products "
            "WHERE id = :product_id",
            product_id = product_id
        )

        return inv[0][0] >= quantity[0][0]
