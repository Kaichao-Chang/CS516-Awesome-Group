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
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity "
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
        print(rows)
        return [Seller_purchase(*row) for row in rows]
