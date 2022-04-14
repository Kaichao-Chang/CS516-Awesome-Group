from flask import current_app as app
from flask_login import current_user

class Purchase:
    def __init__(self, oid, uid, sid, sname, price, quantity, completed_status, time_purchased):
        self.oid = oid
        self.uid = uid
        self.sid = sid
        self.sname = sname
        self.price = price
        self.quantity = quantity
        self.completed_status = "Yes" if completed_status else "No" ###?????
        self.time_purchased = time_purchased 

#    @staticmethod
#    def get(id):
#        rows = app.db.execute(
#        '''
#        SELECT id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased
#        FROM Purchases
#        WHERE id = :id''',
#        id=id)
#        return Purchase(*(rows[0])) if rows else None


    @staticmethod
    def get_all_by_uid_since(uid, start_date, end_date, quantity=-1, seller_firstname='%', seller_lastname='%'):
        quantity_check = ""
        if quantity >= 0:
            quantity_check = "HAVING SUM(total_quantity) = %d" % quantity
        
        inter_table = "WITH subquery AS (" \
                    "SELECT order_id as oid, o.uid AS uid, p.seller_id AS sid, CONCAT(u.firstname, ' ', u.lastname) AS sname, SUM(p.unit_price*p.quantity) AS total_price, SUM(p.quantity) AS total_quantity, o.completed_status, o.placed_datetime " \
                    "FROM Purchases AS p, Users AS u,  Orders as o " \
                    "WHERE o.uid = :uid " \
                        "AND o.pur_id = p.id " \
                        "AND u.id = p.seller_id " \
                        "AND ( ( o.placed_datetime >= :start_date AND o.placed_datetime <= :end_date ) )" \
                        "AND ( ( (u.firstname) LIKE :firstname AND (u.lastname) LIKE :lastname ) ) "\
                    "GROUP BY order_id, o.uid, p.seller_id, u.firstname, u.lastname, o.completed_status, o.placed_datetime ) "\
                "SELECT oid, uid, ARRAY_AGG(sid) AS sidList, ARRAY_AGG(sname) AS sellersList, SUM(total_price) AS total_price_all_sellers, SUM(total_quantity) AS total_quantity_all_sellers, completed_status, placed_datetime "\
                "FROM subquery " \
                "GROUP BY oid, uid, completed_status, placed_datetime "\
                "%s " % (quantity_check) + \
                "ORDER BY placed_datetime DESC "
        rows = app.db.execute(inter_table,
                              uid=uid,
                              start_date=start_date,
                              end_date=end_date,
                              firstname=seller_firstname,
                              lastname=seller_lastname)
        return [Purchase(*row) for row in rows]


    # # may have bugs here:
    # @staticmethod
    # def add_new_purchases(item, id):
    #     app.db.execute('''
    #         INSERT INTO Purchases(id, pid, seller_id, quantity)
    #         VALUES(:id, :pid, :seller_id, :quantity)
    #     ''',
    #     id=id,
    #     pid=item.pid,
    #     seller_id=item.seller_id,
    #     quantity=item.quantity
    #     )