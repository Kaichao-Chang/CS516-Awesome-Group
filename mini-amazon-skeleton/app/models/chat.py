from flask import current_app as app


class Chat:
    def __init__ (self, uid, seller_id, order_id, msg, from_user, time_of_message):
        self.uid = uid
        self.seller_id = seller_id 
        self.msg = msg
        self.order_id = order_id 
        self.from_user = from_user
        self.time_of_message = time_of_message

    @staticmethod 
    def new_message(uid, pur_id, msg):
        seller_id = app.db.execute (
            "SELECT seller_id "
            "FROM Purchases "
            "WHERE id = :pur_id ",
            pur_id = pur_id
        )

        seller_id = seller_id[0][0]

        app.db.execute(
            "INSERT INTO Messages (uid, seller_id, pur_id, msg, from_user) "
            "VALUES(:uid, :seller_id, :pur_id, :msg, TRUE) ",
            uid = uid,
            seller_id = seller_id,
            pur_id = pur_id,
            msg = msg
        )

    @staticmethod 
    def new_message2(uid, pur_id, msg):
        seller_id = app.db.execute (
            "SELECT seller_id "
            "FROM Purchases "
            "WHERE id = :pur_id ",
            pur_id = pur_id
        )

        seller_id = seller_id[0][0]

        app.db.execute(
            "INSERT INTO Messages (uid, seller_id, pur_id, msg, from_user) "
            "VALUES(:uid, :seller_id, :pur_id, :msg, FALSE) ",
            uid = uid,
            seller_id = seller_id,
            pur_id = pur_id,
            msg = msg
        )

    @staticmethod 
    def get_all(pur_id):
        rows = app.db.execute (
            "SELECT uid, seller_id, pur_id, msg, from_user, time_of_message "
            "FROM Messages "
            "WHERE pur_id = :pur_id ",
            pur_id = pur_id
        )

        return [Chat(*row) for row in rows]