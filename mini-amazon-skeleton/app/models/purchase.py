from flask import current_app as app
from flask_login import current_user

class Purchase:
    def __init__(self, id, uid, seller_id, sname, price, quantity, fulfill_by_seller, time_purchased):
        self.id = id
        self.uid = uid
        self.seller_id = seller_id
        self.sname = sname
        self.price = price
        self.quantity = quantity
        self.fulfill_by_seller = "Have Fulfilled" if fulfill_by_seller else "Not yet fulfilled"
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
        
        quantity_check = ""
        if quantity >= 0:
            quantity_check = "HAVING SUM(total_quantity) = %d" % quantity
        
        query = "WITH subquery AS (" \
                    "SELECT p.id, p.uid, p.seller_id, CONCAT(u.firstname, ' ', u.lastname) AS sname, SUM(prod.price*p.quantity) AS total_price, SUM(p.quantity) AS total_quantity, p.fulfill_by_seller, p.time_purchased " \
                    "FROM Purchases AS p, Users AS u, Products AS prod " \
                    "WHERE p.uid = :uid " \
                        "AND p.seller_id = u.id " \
                        "AND p.pid = prod.id " \
                        "AND ( ( p.time_purchased >= :start_date AND p.time_purchased <= :end_date ) OR p.time_purchased IS NULL )" \
                        "AND ( ( LOWER(u.firstname) LIKE :firstname AND LOWER(u.lastname) LIKE :lastname ) OR ( LOWER(u.firstname) LIKE :lastname AND LOWER(u.lastname) LIKE :firstname ) ) "\
                "GROUP BY p.id, p.uid, p.seller_id, u.firstname, u.lastname, p.fulfill_by_seller, p.time_purchased ) "\
                "SELECT id, uid, ARRAY_AGG(seller_id) AS sidList, ARRAY_AGG(sname) AS sellersList, SUM(total_price) AS total_price_all_sellers, SUM(total_quantity) AS total_quantity_all_sellers, fulfill_by_seller, time_purchased "\
                "FROM subquery " \
                "GROUP BY id, uid, fulfill_by_seller, time_purchased "\
                "%s " % (quantity_check) + \
                "ORDER BY time_purchased DESC "
        rows = app.db.execute(query,
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