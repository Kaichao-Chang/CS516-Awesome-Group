from flask import current_app as app


class Order:
    def __init__(self, order_id, total_items, total_fulfill, time_placed, price):
        self.order_id = order_id
        self.time_placed = time_placed
        self.total_items = total_items 
        self.total_fulfill = total_fulfill
        self.price = price
    
    @staticmethod 
    def get_all_by_user (uid):
        order_infos = app.db.execute(
            "WITH temp AS ( "
            "SELECT Orders.order_id, MIN(Purchases.time_purchased) AS time_purchased "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            "GROUP BY Orders.order_id "
            ") "
            "SELECT Orders.order_id, COUNT(*), SUM(CASE WHEN fulfill_by_seller THEN 1 ELSE 0 END), temp.time_purchased, SUM(quantity * unit_price) "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            "LEFT JOIN temp "
            "ON Orders.order_id = temp.order_id "
            "WHERE Orders.uid = :uid "
            "GROUP BY Orders.order_id, temp.time_purchased "
            "ORDER BY temp.time_purchased DESC"
            ,uid = uid 
        )
        return [Order(*order_info) for order_info in order_infos]

    @staticmethod 
    def get_purchase_time (oid):
        purchase_time = app.db.execute(
            "SELECT MIN(Purchases.time_purchased) AS time_purchased "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            "WHERE Orders.order_id = :oid ",
            oid = oid)

        return purchase_time

    @staticmethod 
    def get_total_price (oid):
        total_price = app.db.execute(
            "SELECT SUM(quantity * unit_price) "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            "WHERE Orders.order_id = :oid ",
            oid = oid)

        return total_price

    @staticmethod 
    def get_order_id(pur_id):
        order_id = app.db.execute(
            "SELECT order_id "
            "FROM Orders "
            "WHERE pur_id = :pur_id ",
            pur_id = pur_id
        )

        return order_id[0][0]
class Detailed_Order: 
    def __init__(self, pur_id, p_name, quantity, unit_price, seller_lname, seller_fname, fulfill_by_seller, fulfill_time):
        self.pur_id = pur_id
        self.p_name = p_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.seller_lname = seller_lname
        self.seller_fname = seller_fname
        self.fulfill_by_seller = fulfill_by_seller
        self.fulfill_time = fulfill_time

    @staticmethod 
    def get_all_by_oid (oid):
        detailed_order = app.db.execute(
            "SELECT Purchases.id, Products.name, Purchases.quantity, Purchases.unit_price, Users.lastname, Users.firstname, Purchases.fulfill_by_seller, Order_fulfill.time_fulfilled "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Users "
            "ON Products.seller_id = Users.id "
            "LEFT JOIN Order_fulfill "
            "ON Order_fulfill.id = Purchases.id "
            "WHERE Orders.order_id = :oid",
            oid = oid
        )
        return [Detailed_Order(*order_info) for order_info in detailed_order]
    