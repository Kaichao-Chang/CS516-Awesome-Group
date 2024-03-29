from flask import current_app as app

class Product_page():

    def get_product(id):
        name = app.db.execute(
            '''
Select name
From Products
Where id = :id
            ''', id=id)
        name = name[0][0]
        return app.db.execute(
                     '''
SELECT Products.*, CONCAT(Users.firstname, ' ', Users.lastname) AS seller_name
FROM Products
LEFT JOIN Users ON Products.seller_id = Users.id
WHERE available = True and name = :name
ORDER BY price
            ''', name=name), name