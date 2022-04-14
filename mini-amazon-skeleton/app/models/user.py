from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask import current_app as app
from .. import login
from datetime import datetime


class User(UserMixin):

    class Review:
        def __init__(self, content, star, upvote, customer_id):
            self.content = content 
            self.star = star
            self.upvote = upvote
            self.customer_id = customer_id

    def __init__(self, id, email, firstname, lastname, address, is_seller, content=[], star=[], upvote=[], customer_id=[]):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.is_seller = False if is_seller is None else True
        self.reviews = []

        if self.is_seller:
            for a, _ in enumerate(content):
                if _ is not None:
                    rev_full = self.Review(content[a], star[a], upvote[a], customer_id[a])
                    self.reviews.append(rev_full)


    # requirement 1: an existing user can log in using email and password.
        # if the password and email are correct, this function will return the users' information
    @staticmethod
    def get_by_auth(email, password):     
        rows = app.db.execute(
            """
            select password, id, email, firstname, lastname, address, False AS is_seller
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

    # This function will return the user object;  if the user does not exist, it will retur None.
    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
        SELECT u.id, email, firstname, lastname, address,
        CASE WHEN u.id in (SELECT uid FROM Sellers) THEN true 
        ELSE false
        END AS is_seller,
        ARRAY_AGG(content), ARRAY_AGG(star), ARRAY_AGG(upvote), ARRAY_AGG(customer_id)
        FROM Users AS u
        LEFT JOIN SellerReviews AS s
        ON u.id = s.seller_id
        WHERE u.id = :id
        GROUP BY u.id, email, firstname, lastname, address, s.seller_id """,
        id=id)
        return User(*(rows[0])) if rows else None


    def buildup_profile(self, email, firstname, lastname, address):
        self.email = email 
        self.firstname = firstname
        self.lastname = lastname
        self.address = address

    # requirement 2: Users can update all information except the id.
        # after updating the user's information, this function will return the user's unique id
    @staticmethod
    def update_infor (email, firstname, lastname, address):
        try:
            id = current_user.id
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
    def update_password(password):
        id = current_user.id
        rows = app.db.execute(
            """
            update Users
            set password = :password
            where id = :id
            returning id""",
        password=generate_password_hash(password),
        id=id)
        id = rows[0][0]
        return User.get(id)


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

    # requirement 3: Each account is associated with a balance. 
        # It starts out as $0, but can be topped up by the user. 
        # The user can also withdraw up to the full balance. 
    @staticmethod
    def update_balance(id, topup, withdraw):
        # In this case, the balance can be negative values (it's similar as credit card debit - if it'negative, you owe our company money)
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
