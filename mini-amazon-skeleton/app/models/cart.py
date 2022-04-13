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