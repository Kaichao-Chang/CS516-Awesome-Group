from flask import current_app as app

class Search():
        order = None
        keyword = None
        cate = None

        @staticmethod
        def search_product(search_msg, cate, order):
                sql = """
SELECT Products.*, CONCAT(Users.firstname, ' ', Users.lastname) as seller_name
FROM Products 
LEFT JOIN Users ON Products.seller_id = Users.id
"""
               
                Search.keyword = search_msg
                Search.order = order
                Search.cate = cate

                if search_msg and cate:
                        sql += \
                        """
WHERE (name LIKE '%{}%' or descr LIKE '%{}%')
AND cate = '{}'
AND available = True
                        """.format(search_msg, search_msg, cate)
                
                elif search_msg:
                        sql += \
                        """
WHERE (name LIKE '%{}%' or descr LIKE '%{}%')
AND available = True
                        """.format(search_msg, search_msg)
                elif cate:
                        sql += \
                        """
WHERE cate = '{}'
AND available = True
                        """.format(cate)

                else:
                        sql += 'Where available = True\n'
                if order == 1:
                        sql += "ORDER BY price"
                elif order == 2:
                        sql += "ORDER BY price DESC"
                print(sql)
                return app.db.execute(sql)

class Order_Search:
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
        def search_order(uid, search_msg,  fulfill):
                sql = """
SELECT Purchases.id, Users.id, Users.firstname, Users.lastname, Users.address, Purchases.pid, Purchases.seller_id, Purchases.quantity, Purchases.fulfill_by_seller, Purchases.time_purchased, Products.name, Products.price * Purchases.quantity, Order_fulfill.time_fulfilled 
From Purchases 
LEFT JOIN Users  
ON Purchases.uid = Users.id 
LEFT JOIN Products 
ON Purchases.pid = Products.id 
LEFT JOIN Order_fulfill 
ON Purchases.id = Order_fulfill.id 
"""     
                sql += \
                        """
WHERE ( CONCAT(Users.firstname, ' ', Users.lastname)  LIKE '%{}%' or Products.name LIKE '%{}%')
                        """.format(search_msg, search_msg)
                if fulfill == 0:
                        sql += \
                                """
AND Purchases.seller_id = {}
ORDER BY time_purchased DESC        
                                """.format(uid)
                
                if fulfill == 1:
                        sql += \
                                """
AND Purchases.seller_id = {}
AND  Purchases.fulfill_by_seller = TRUE
ORDER BY time_purchased DESC        
                                """.format(uid)

                if fulfill == 2:
                        sql += \
                                """
AND Purchases.seller_id = {}
AND  Purchases.fulfill_by_seller = FALSE
ORDER BY time_purchased DESC        
                                """.format(uid)
                
                rows = app.db.execute(sql)
                return [Order_Search(*row) for row in rows]
    
               
              