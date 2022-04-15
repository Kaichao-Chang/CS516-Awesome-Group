from flask import current_app as app
import matplotlib.pyplot as plt
import os
from werkzeug.utils import secure_filename
import uuid

class Seller_purchase:
    def __init__(self, id, uid, buyer_fname, buyer_lname, buyer_addr, pid, seller_id, quantity, fulfilled_by_seller, time_purchased, p_name, price, time_fulfilled):
        self.id = id
        self.uid = uid
        self.buyer_fname = buyer_fname
        self.buyer_lname = buyer_lname
        self.buyer_addr = buyer_addr
        self.pid = pid
        self.seller_id = seller_id
        self.quantity = quantity
        self.fulfilled_by_seller = fulfilled_by_seller
        self.time_purchased = time_purchased
        self.p_name = p_name
        self.price = price 
        self.time_fulfilled = time_fulfilled

    @staticmethod
    def get_all_by_seller(uid):
        rows = app.db.execute(
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled "
            "From Purchases "
            "LEFT JOIN Users  "
            "ON Purchases.uid = Users.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Order_fulfill "
            "ON Purchases.id = Order_fulfill.id "
            "WHERE Purchases.seller_id = :uid "
            "ORDER BY time_purchased DESC",
                              uid=uid)
        return [Seller_purchase(*row) for row in rows]
    
    @staticmethod
    def get_all_by_purchaseid(uid, purchases_id):
        rows = app.db.execute(
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled "
            "From Purchases "
            "LEFT JOIN Users  "
            "ON Purchases.uid = Users.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Order_fulfill "
            "ON Purchases.id = Order_fulfill.id "
            "WHERE Purchases.seller_id = :uid "
            "AND Purchases.id = :purchases_id "
            "ORDER BY time_purchased DESC",
                              uid=uid,
                              purchases_id = purchases_id)
        return [Seller_purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_product(pid, uid):
        rows = app.db.execute(
            "SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled "
            "From Purchases "
            "LEFT JOIN Users  "
            "ON Purchases.uid = Users.id "
            "LEFT JOIN Products "
            "ON Purchases.pid = Products.id "
            "LEFT JOIN Order_fulfill "
            "ON Purchases.id = Order_fulfill.id "
            "WHERE Purchases.seller_id = :uid "
            "AND Products.id = :pid "
            "ORDER BY time_purchased DESC",
                              uid=uid,
                              pid = pid)
        return [Seller_purchase(*row) for row in rows]

    @staticmethod
    def get_product_name(pid):
        p_name = app.db.execute(
            "SELECT name "
            "FROM Products "
            "WHERE id = :pid",
            pid = pid)
        
        return p_name

    @staticmethod
    def order_fulfill(id, uid):
        app.db.execute(
            "UPDATE purchases "
            "SET fulfill_by_seller = true "
            "WHERE id = :id",
            id = id 
        )

        app.db.execute(
            "INSERT INTO order_fulfill(id, time_fulfilled) "
            "VALUES (:id, now()::timestamp)",
            id = id)
        
        old_balance = app.db.execute(
            "SELECT balance "
            "FROM Users "
            "WHERE id = :uid ",
            uid = uid
        )

        old_balance = old_balance[0][0]

        earn = app.db.execute(
            "SELECT quantity* unit_price "
            "FROM Purchases "
            "WHERE id = :id ",
            id = id
        )

        earn = earn[0][0]
        new_balance = old_balance + earn 

        app.db.execute (
            "UPDATE Users "
            "SET balance = :new_balance "
            "WHERE id = :uid ",
            new_balance = new_balance,
            uid = uid
        )

        product_id = app.db.execute(
            "SELECT pid "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        product_id = product_id[0][0]

        quantity = app.db.execute(
            "SELECT quantity "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        inv = app.db.execute(
            "SELECT inv "
            "FROM Products "
            "WHERE id = :product_id",
            product_id = product_id
        )

        new_inv = inv[0][0] - quantity[0][0]

        app.db.execute(
            "UPDATE Products "
            "SET inv = :new_inv "
            "WHERE id = :product_id",
            product_id = product_id,
            new_inv = new_inv
        )

    @staticmethod
    def enough_inv(id):
        
        product_id = app.db.execute(
            "SELECT pid "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        product_id = product_id[0][0]

        quantity = app.db.execute(
            "SELECT quantity "
            "FROM Purchases "
            "WHERE id = :id",
            id = id)

        inv = app.db.execute(
            "SELECT inv "
            "FROM Products "
            "WHERE id = :product_id",
            product_id = product_id
        )

        return inv[0][0] >= quantity[0][0]

    @staticmethod
    def pie_chart(id):
        labels = 'Remaining Inventory', 'Quantity Already Sold'

  
        quantity = app.db.execute(
            "SELECT COALESCE(SUM(quantity), 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = TRUE",
            id = id)

        inv = app.db.execute(
            "SELECT COALESCE(inv, 0) "
            "FROM Products "
            "WHERE id = :id",
            id = id
        )
 

        sizes = [inv[0][0], quantity[0][0]]
        explode = (0, 0.1)  
        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct= '%1.1f%%', startangle=90)
        ax.axis('equal') 
        
        filename = str(uuid.uuid4())
        
        fig.savefig(os.path.join(
            app.instance_path,'../app/static/analysis_pic/' , filename
        ))
        plt.close(fig)

        return filename
    
    @staticmethod
    def running_low(id):

        quantity = app.db.execute(
            "SELECT COALESCE(SUM(quantity), 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = TRUE",
            id = id)

        inv = app.db.execute(
            "SELECT COALESCE(inv, 0) "
            "FROM Products "
            "WHERE id = :id",
            id = id
        )

        r_l = inv[0][0]/(inv[0][0] +quantity[0][0]) < 0.2

        return r_l

    @staticmethod
    def bar_chart(id):
        labels = ['Fulfilled quantity', 'Unfulfilled quantity', 'remaining inventory']

  
        fquantity = app.db.execute(
            "SELECT COALESCE(SUM(quantity), 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = TRUE",
            id = id)

        ufquantity = app.db.execute(
            "SELECT COALESCE(SUM(quantity), 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = FALSE",
            id = id)

        inv = app.db.execute(
            "SELECT COALESCE(inv, 0) "
            "FROM Products "
            "WHERE id = :id",
            id = id
        )

        fig = plt.figure(figsize = (5,7))

        sizes = [fquantity[0][0], ufquantity[0][0], inv[0][0]]

        plt.bar(labels, sizes, linewidth = 0.3, width = 0.5, facecolor = 'lightskyblue')
        
        for a,b in zip(labels, sizes):

            plt.text(a, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)

        filename = str(uuid.uuid4())
        
        fig.savefig(os.path.join(
            app.instance_path,'../app/static/analysis_pic/' , filename
        ))
        plt.close(fig)

        return filename

    @staticmethod
    def running_low_1(id):

        ufquantity = app.db.execute(
            "SELECT COALESCE(SUM(quantity), 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = FALSE",
            id = id)

        inv = app.db.execute(
            "SELECT COALESCE(inv, 0) "
            "FROM Products "
            "WHERE id = :id",
            id = id
        )

        r_l = inv[0][0] < ufquantity[0][0]

        return r_l

    @staticmethod
    def line_chart(id):

  
        quantity = app.db.execute(
            "SELECT COALESCE(quantity, 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = TRUE "
            "ORDER BY time_purchased DESC",
            id = id)

        time = app.db.execute(
            "SELECT time_purchased "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = TRUE "
            "ORDER BY time_purchased DESC",
            id = id
        )
        fig = plt.figure()
        plt.plot(time, quantity, 'b*-', label = 'Order Fuifullment Time Trend')
        plt.legend()
        filename = str(uuid.uuid4())
        fig.savefig(os.path.join(
            app.instance_path,'../app/static/analysis_pic/' , filename
        ))
        plt.close(fig)

        return filename

    @staticmethod
    def draw_line_chart(id):

  
        quantity = app.db.execute(
            "SELECT COALESCE(quantity, 0) "
            "FROM Purchases "
            "WHERE pid = :id "
            "AND fulfill_by_seller = TRUE "
            "ORDER BY time_purchased DESC",
            id = id)

        draw = len(quantity) > 0

        return draw