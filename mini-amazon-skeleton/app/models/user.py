# https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask
from flask_login import UserMixin
# https://blog.csdn.net/h18208975507/article/details/108106506
from werkzeug.security import check_password_hash
# https://werkzeug.palletsprojects.com/en/1.0.x/utils/
from werkzeug.security import generate_password_hash

from flask_login import current_user
from flask import current_app as app

from .. import login


# https://stackoverflow.com/questions/63231163/what-is-the-usermixin-in-flask
# https://flask-login.readthedocs.io/en/latest/#your-user-class
class User(UserMixin):

    def __init__(self, id, email, firstname, lastname, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address

    # requirement 1: an existing user can log in using email and password.
        # if the password and email are correct, this function will return the users' information
    @staticmethod
    def get_by_auth(email, password):     
        rows = app.db.execute(
            """
            select password, id, email, firstname, lastname, address
            from Users
            where email = :email""", 
            email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))
    
    # requirement 1: check if the password the user input is correct
        # if the password and email are correct, this function will return True; else, False
    @staticmethod
    def pw_right_or_wrong(email, password):
        rows = app.db.execute(
        """
        select password
        from Users
        where email = :email
        """,
        email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # correct password
            return False
        else:
            return True

    # requirement 2: find the corresponding email, if id is given
        # if the id exists in table Users, this function will return the unique email of this user
    @staticmethod
    def get_email(id):
        rows = app.db.execute(
        """
        select email
        from Users
        where id = :id
        """,
        id=id)
        if not rows:  # email not found
            return None
        else:
            return rows[0][0]

    # requirement 2: Ensure that email is unique among all users.
        # return true, if there is the same email exists in the table Users.
    @staticmethod
    def email_exists(email):    
       
        rows = app.db.execute(
            """
            select email
            from Users
            where email = :email""",
            email=email)
        return len(rows) > 0

    # requirement 1: A new user can register for a new account.
        # if there is no error, the table Users will be updated
    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute(
            """
            INSERT INTO Users(email, password, firstname, lastname, address)
            VALUES(:email, :password, :firstname, :lastname, :address)
            RETURNING id""",
            email=email,
            password=generate_password_hash(password),
            firstname=firstname, 
            lastname=lastname, 
            address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
        
    # requirement 2: Each user account has a system-assigned id.
    @staticmethod
    @login.user_loader
    def get(id):
    # input of the function get_id is a user's id, and the output is a user's object, 
    # including users' infor like id, email, firstname, and lastname.
        rows = app.db.execute(
        """
        SELECT id, email, firstname, lastname, address, SellerReviews.id
        FROM Users
        LEFT JOIN SellerReviews ON id = SellerReviews.id
        WHERE id = :id
        GROUP BY id, email, firstname, lastname, address, SellerReviews.id""",
        id=id)
        return User(*(rows[0])) if rows else None

    # requirement 2: Users can update all information except the id.
        # after updating the user's information, this function will return the user's unique id
    @staticmethod
    def update_infor(id, email, firstname, lastname, address):
        try:
            rows = app.db.execute(
            """
            UPDATE Users
            SET email = :email, firstname = :firstname, lastname = :lastname, address = :address
            WHERE id = :id
            RETURNING id""",
            email=email,
            firstname=firstname, 
            lastname=lastname,
            address=address,
            id=id)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None
    
    # requirement 2: Users can update the password. 
        # after updating the user's password, this function will return the user's unique id
    @staticmethod
    def update_password(id, password):
        rows = app.db.execute(
        """
        UPDATE Users
        SET password = :password
        WHERE id = :id
        RETURNING id""",
        password=generate_password_hash(password),
        id=id)
        id = rows[0][0]
        return User.get(id)

    # requirement 3: Each account is associated with a balance. 
        # It starts out as $0, but can be topped up by the user. 
        # The user can also withdraw up to the full balance. 
    @staticmethod
    def balance_change(id, topup, withdraw):
        try:
            rows = app.db.execute(
            """
            UPDATE Users
            SET balance = balance + :change
            WHERE id = :id
            RETURNING id""",
            change=(topup-withdraw),
            id=id)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(e)
            return None

    # requirement 3: find the corresponding account balance, if id is given
        # if the id exists in table Users, this function will return the corresponding balance of that user
    @staticmethod
    def get_balance(id):
        rows = app.db.execute(
        """
        SELECT balance
        FROM Users
        WHERE id = :id""",
        id=id)
        return rows[0][0]

    
    

'''
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname)
VALUES(:email, :password, :firstname, :lastname)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
'''

