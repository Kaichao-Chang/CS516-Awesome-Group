from flask import current_app as app
from flask_login import current_user

class Purchase:
    def __init__(self, oid, uid, sid, sname, price, quantity, time_purchased):
        self.oid = oid
        self.uid = uid
        self.sid = sid
        self.sname = sname
        self.price = price
        self.quantity = quantity
        # self.fulfill_by_seller = "Have Fulfilled" if fulfill_by_seller else "Not yet fulfilled"
        self.time_purchased = time_purchased # or: self.time_purchased = "NA (not completed)" if time_purchased == None else time_purchased

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
        inter_table = "WITH subquery AS (" \
                    "SELECT order_id as oid, p.id AS id, p.uid AS uid, p.seller_id AS sid, CONCAT(u.firstname, ' ', u.lastname) AS sname, SUM(p.unit_price*p.quantity) AS total_price, SUM(p.quantity) AS total_quantity, p.time_purchased AS time_purchased " \
                    "FROM Purchases AS p, Users AS u,  Orders as o " \
                    "WHERE o.uid = :uid " \
                        "AND o.pur_id = p.id " \
                        "AND p.seller_id = u.id " \
                        "AND ( ( p.time_purchased >= :start_date AND p.time_purchased <= :end_date ) )" \
                        "AND ( ( LOWER(u.firstname) LIKE :firstname AND LOWER(u.lastname) LIKE :lastname ) OR ( LOWER(u.firstname) LIKE :lastname AND LOWER(u.lastname) LIKE :firstname ) ) "\
                    "GROUP BY order_id, p.id, p.uid, p.seller_id, u.firstname, u.lastname, p.time_purchased ) "\
                "SELECT oid, uid, ARRAY_AGG(sid) AS sidList, ARRAY_AGG(sname) AS sellersList, SUM(total_price) AS total_price_all_sellers, SUM(total_quantity) AS total_quantity_all_sellers, MAX(time_purchased) AS time_purchased "\
                "FROM subquery " \
                "GROUP BY oid, uid "\
                "ORDER BY time_purchased DESC "
        rows = app.db.execute(inter_table,
                              uid=uid,
                              start_date=start_date,
                              end_date=end_date,
                              firstname=seller_firstname,
                              lastname=seller_lastname)
        return [Purchase(*row) for row in rows]










    # may have bugs here:
    @staticmethod
    def add_new_purchases(item, id):
        app.db.execute('''
            INSERT INTO Purchases(id, pid, seller_id, quantity)
            VALUES(:id, :pid, :seller_id, :quantity)
        ''',
        id=id,
        pid=item.pid,
        seller_id=item.seller_id,
        quantity=item.quantity
        )