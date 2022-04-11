from flask import current_app as app

class Search():
        order = None
        keyword = None
        cate = None

        @staticmethod
        def search_product(search_msg, cate, order):
                sql = """
SELECT *
FROM Products """
               
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