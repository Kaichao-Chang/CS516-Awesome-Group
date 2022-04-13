from flask import current_app as app
from flask_login import current_user

class Purchase:
    def __init__(self, id, uid, pid, seller_id, seller_name, price, quantity, fulfill_by_seller, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.price = price
        self.quantity = quantity
        self.fulfill_by_seller = "Have Fulfilled" if fulfill_by_seller else "Not yet fulfilled"
        self.time_purchased = time_purchased # or: self.time_purchased = "NA (not completed)" if time_purchased == None else time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute(
        '''
        SELECT id, uid, pid, seller_id, quantity, fulfill_by_seller, time_purchased
        FROM Purchases
        WHERE id = :id''',
        id=id)
        return Purchase(*(rows[0])) if rows else None

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

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute(
                '''
                WITH t1 AS (
                    SELECT p.id AS id, p.uid AS uid, p.seller_id AS seller_id, CONCAT(u.firstname, ' ', u.lastname) AS seller_name, SUM(prod.price*p.quantity) AS total_amount, SUM(quantity) AS total_quantity, p.fulfill_by_seller AS fulfill_by_seller, p.time_purchased AS time_purchased 
                    FROM Purchases AS p, Users AS u, Products AS prod
                    WHERE p.uid = :uid
                    AND u.id = p.seller_id 
                    AND prod.id = p.pid
                    And time_purchased >= :since
                    GROUP BY p.id, p.uid, p.seller_id, u.firstname, u.lastname, p.fulfill_by_seller, p.time_purchased)

                SELECT t1.id AS id, t1.uid AS uid, ARRAY_AGG(t1.seller_id) AS seller_id_List, ARRAY_AGG(t1.seller_name) AS seller_name_List, SUM(t1.total_amount) AS total_amount_all_sellers, SUM(t1.total_quantity) AS total_quantity_all_sellers, t1.fulfill_by_seller AS fulfill_by_seller, t1.time_purchased AS time_purchased
                FROM t1
                GROUP BY id, uid, fulfill_by_seller, time_purchased
                ORDER BY t1.time_purchased DESC
                ''',
                uid=uid,
                since=since)
        return [Purchase(*row) for row in rows]
