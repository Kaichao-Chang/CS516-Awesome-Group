from flask import current_app as app


class Seller_purchase:
    def __init__(self, id, uid, pid, seller_id, quantity, fulfilled_by_seller, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.seller_id = seller_id
        self.quantity = quantity
        self.fulfilled_by_seller = fulfilled_by_seller
        self.time_purchased = time_purchased

    @staticmethod
    def get_all_by_seller(uid):
        rows = app.db.execute(
            "SELECT * "
            "From Purchases "
            "WHERE seller_id = :uid "
            "ORDER BY time_purchased DESC",
                              uid=uid)
        return [Seller_purchase(*row) for row in rows]
