from flask import current_app as app
from flask_login import current_user

class Purchase:
    def __init__(self, oid, uid, completed_status, time_purchased, sid, sname, price, quantity):
        self.oid = oid
        self.uid = uid
        self.sid = sid
        self.sname = sname
        self.price = price
        self.quantity = quantity
        self.completed_status = "Have Completed :)" if completed_status else "Not Completed :(" 
        self.time_purchased = time_purchased 

    @staticmethod
    def get_all_by_uid_since(uid, start_date, end_date, quantity=-1, seller_firstname='%', seller_lastname='%'):
        rows = app.db.execute(
            '''
            WITH subquery AS (
                    SELECT order_id as oid, o.uid AS uid, p.seller_id AS sid, CONCAT(u.firstname, ', ', u.lastname) AS sname, SUM(p.unit_price*cast(p.quantity AS DECIMAL(7,2) )) AS total_price, SUM(p.quantity) AS total_quantity, o.completed_status, o.placed_datetime
                    FROM Orders as o, Purchases AS p, Users AS u, 
                    WHERE o.uid = :uid 
                    AND o.pur_id = p.id AND u.id = p.seller_id AND ( ( o.placed_datetime >= :start_date AND o.placed_datetime <= :end_date ) )
                    GROUP BY order_id, o.uid, p.seller_id, u.firstname, u.lastname, o.completed_status, o.placed_datetime 
                    )
                SELECT oid, uid, completed_status, MIN(placed_datetime) AS time_purchased, ARRAY_AGG(sid) AS sid, ARRAY_AGG(sname) AS sname, SUM(total_price) AS price, SUM(total_quantity) AS quantity
                FROM subquery 
                GROUP BY oid, uid, completed_status
                ORDER BY MIN(placed_datetime) DESC
            ''',
            uid=uid,
            start_date=start_date,
            end_date=end_date,
            firstname=seller_firstname,
            lastname=seller_lastname)
        return rows