from ast import Not
from pickle import FALSE, NONE, TRUE
from flask_login import UserMixin, current_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

class Seller(UserMixin):
    def __init__(self, uid):
        self.uid = uid

    @staticmethod
    def is_seller(uid):
        rows = app.db.execute(
        """
        SELECT *
        FROM sellers
        WHERE uid = :uid
        """, uid = uid)
        return len(rows) > 0
        

    @staticmethod
    def seller_register(uid):
        try:
            if not Seller.is_seller(uid):
                   rows = app.db.execute(
                    """
                    INSERT INTO Sellers(uid)
                    VALUES(:uid)       
                    RETURNING id
                    """, uid = uid)
            return None
        except Exception as e:
            print(str(e))
            return None
            
            