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
            "SELECT DISTINCT order_id, DISTINCT time_purchased "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            ") "
            "SELECT Orders.order_id, COUNT "
            "FROM Orders "
            "LEFT JOIN Purchases "
            "ON Orders.pur_id = Purchases.id "
            "LEFT JOIN temp "
            "ON Orders.order_id = temp.order_id "
            "WHERE Orders.uid = : uid "
            "GROUP BY Orders.order_id "
            "ORDER BY Or temp.time_purchased ",
            uid = uid 
        )
        return [Order(*order_info) for order_info in order_infos]

