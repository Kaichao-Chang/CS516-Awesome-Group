from flask import current_app as app

class Search():
    @staticmethod
    def search_product(search_msg):
        rows = app.db.execute("""
SELECT *
FROM Products
WHERE name LIKE '%{}%'
""".format(search_msg))
        print("""
SELECT *
FROM Products
WHERE name LIKE '%{}%'
""".format(search_msg))
        print(rows)
        return rows