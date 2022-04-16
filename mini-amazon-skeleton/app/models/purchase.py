from flask import current_app as app

class Purchase:
    def __init__(self, id, uid, completed_status, time_purchased, sid, sname, price, quantity):
        self.id = id
        self.uid = uid
        self.completed_status = "Have Completed :)" if completed_status else "Not Completed :("
        self.time_purchased = time_purchased
        self.sid = sid
        self.sname = sname
        self.price = price
        self.quantity = quantity

    @staticmethod
    def get_all_by_uid_since(uid, start_date, end_date, seller_firstname='%', seller_lastname='%'):
        rows = app.db.execute(
            '''
            WITH subquery AS (
                    SELECT order_id as id, o.uid AS uid, p.seller_id AS sid, o.completed_status, o.placed_datetime, CONCAT(u.firstname, '_', u.lastname) AS sname, SUM(p.unit_price*cast(p.quantity AS DECIMAL(7,2) )) AS total_price, SUM(p.quantity) AS total_quantity
                    FROM Orders as o
                    left join Purchases AS p
                    on o.pur_id = p.id
                    left join Users AS u
                    on p.seller_id = u.id
                    WHERE o.uid = :uid 
                        AND ( ( o.placed_datetime > :start_date AND o.placed_datetime < :end_date ) )
                    GROUP BY order_id, o.uid, p.seller_id, u.firstname, u.lastname, o.completed_status, o.placed_datetime 
                    )
                SELECT id, uid, completed_status, MIN(placed_datetime) AS time_purchased, ARRAY_AGG(sid) AS sid, ARRAY_AGG(sname) AS sname, SUM(total_price) AS price, SUM(total_quantity) AS quantity
                FROM subquery 
                GROUP BY id, uid, completed_status
                ORDER BY MIN(placed_datetime) DESC
            ''',
            uid=uid,
            start_date=start_date,
            end_date=end_date,
            firstname=seller_firstname,
            lastname=seller_lastname)
        return rows