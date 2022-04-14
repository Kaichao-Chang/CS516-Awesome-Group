from flask import current_app as app

class Cart():

        @staticmethod
        def get_cart(uid):
            cart = app.db.execute( """
Select Cart.pid, Products.name, Products.price, CONCAT(Users.firstname, ' ', Users.lastname) as seller_name, Cart.quantity
From Cart
LEFT JOIN Products ON Products.id = Cart.pid
LEFT JOIN Users ON Products.seller_id = Users.id
Where Cart.uid = :uid
""", uid = uid)
            return cart

        @staticmethod
        def add_cart(uid, pid):
            app.db.execute( """
INSERT INTO Cart(uid, pid, quantity)
SELECT :uid, :pid, 1
WHERE 
    NOT EXISTS (
        SELECT id
        FROM Cart
        WHERE uid=:uid AND pid=:pid
);
""", uid=uid, pid=pid)

        @staticmethod
        def change_cart(uid, pid, quantity):
            app.db.execute( """
UPDATE Cart
Set quantity = :quantity
Where uid = :uid AND pid = :pid
""", uid=uid, pid=pid, quantity=quantity)

        @staticmethod
        def delete_cart(uid, pid):
            app.db.execute( """
DELETE FROM Cart
Where uid = :uid AND pid = :pid
""", uid=uid, pid=pid)

        @staticmethod
        def checkout(uid):
            values = app.db.execute( """
Select Cart.uid, Cart.pid, Products.seller_id, Cart.quantity, Products.price
From Cart
LEFT JOIN Products ON Products.id = Cart.pid
Where Cart.uid = :uid
""", uid=uid)
            print("look here",values)
            print("flag")
            for row in values:
                print("row",row)
                app.db.execute("""
    INSERT INTO Purchases (uid, pid, seller_id, quantity, unit_price)
    VALUES (:uid, :pid, :seller_id, :quantity, :unit_price)
    """, uid=row.uid, pid=row.pid, seller_id=row.seller_id, quantity=row.quantity, unit_price=row.price)
            app.db.execute("""
DELETE FROM Cart
Where uid = :uid
""", uid=uid)
            return True