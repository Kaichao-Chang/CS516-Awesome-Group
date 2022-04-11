"""
from flask import current_app as app
from .product import Product
from flask_login import current_user

class Purchase:
    def __init__(self, id, uid, pid, price, quantity, time_purchased, seller_uid):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.price = price
        self.quantity = quantity
        self.seller_uid = seller_uid

    @staticmethod
    def get(id):
        rows = app.db.execute(
        '''
        SELECT pur.id as id, pur.uid as uid, pur.pid as pid, pur.price as price, pur.quantity as quantity, 
            pur.time_purchased as time_purchased, pro.seller_id AS seller_uid
        FROM Purchases pur
        INNER JOIN Products pro ON pur.pid = pro.pid
        WHERE id = :id''',
        id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
        SELECT pur.id, pur.uid, pur.pid, price, time_purchased, pro.seller_id AS seller_uid
        FROM Purchases pur
        INNER JOIN Products pro
        ON pur.pid = pro.id
        WHERE pur.uid = :uid
        AND time_purchased >= :since
        ORDER BY time_purchased DESC''',
        uid=uid,
        since=since)
        return [Purchase(*row) for row in rows]
"""
    
from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, name, price, time_purchased, seller_uid):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.name = name
        self.price = price
        self.seller_uid = seller_uid

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT pur.id, pur.uid, pid, name, price, time_purchased, pro.seller_id AS seller_uid
FROM Purchases pur
INNER JOIN Products pro
    ON pur.pid = pro.id
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT pur.id, pur.uid, pid, name, price, time_purchased, pro.seller_id AS seller_uid
FROM Purchases pur
INNER JOIN Products pro
    ON pur.pid = pro.id
WHERE pur.uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
