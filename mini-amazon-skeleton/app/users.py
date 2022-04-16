from cgi import print_exception
from email.message import Message
from operator import is_
from pydoc import describe
from unicodedata import category, name
from flask import Blueprint, flash, redirect, render_template, request, url_for, flash, Markup, current_app as app, g
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from wtforms import BooleanField, PasswordField, StringField, SubmitField, DecimalField, IntegerField, SelectField, FloatField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, AnyOf, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.widgets.core import HTMLString, html_params, escape
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, date

from .models.user import User
from .models.purchase import Purchase
from .models.seller import Seller
from .models.product import Product, Product2
from .models.seller_purchase import Seller_purchase
from .models.cart import Cart
from .models.social import SellerReview
from .models.order import Order, Detailed_Order
from .models.chat import Chat

import itertools
import datetime
import os

bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Your login email is invalide, or maybe your password is incorrect :(')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data): # Celia added address here
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


####################### The followings are to Update Account ########################
class UpdateProfileForm(FlaskForm): 
    firstname = StringField('Your First Name', validators=[DataRequired('Please enter your first name here:')]) 
    lastname = StringField('Your Last Name', validators=[DataRequired('Please enter your last name here:')])
    email = StringField('Your Email', validators=[DataRequired('Please enter your email address here:'), Email()])
    address = StringField('Your Address', validators=[DataRequired('Please enter your address here:')])
    submit = SubmitField('Update Your Profile')

    def validate_email(self, email):
        if User.email_exists(email.data) and email.data != current_user.email:
            raise ValidationError('Already a user with this email.')

@bp.route('/account', methods=['GET', 'POST'])
def account():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if User.update_infor(form.email.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data):
            flash('Your profile are updated!')
            return redirect(url_for('users.account'))
    return render_template("account.html",  form=form)


class UpdatePasswordForm(FlaskForm): 
    curr_pwd = PasswordField('Your First Name', validators=[DataRequired('Please enter your current password here:')]) 
    new_pwd = PasswordField('Your New Password', validators=[DataRequired('Please enter your new password here:')])   
    retype_pwd = PasswordField('Re-enter Your New Password', validators=[DataRequired('Please re-enter your new password here:'), EqualTo('new_pwd')])
    submit = SubmitField('Update Password')

    def validate_curr_pwd(self,curr_pwd): 
        if User.get_by_auth(current_user.email, curr_pwd.data) is None: 
            raise ValidationError('The current password you input is incorrect.')

@bp.route('/password', methods=['GET', 'POST'])
def password():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if User.update_password(form.new_pwd.data):
            flash('You have changed your password!')
            return redirect(url_for('users.password'))
    return render_template('change_password.html', title='Password', form=form)
        

##################### The follwings are to deal with Balance ##########################
class BalanceForm(FlaskForm):
    topup = DecimalField('deposit', validators=[], default=0)
    withdraw = DecimalField('withdraw', validators=[], default=0)
    submit = SubmitField('Update Your Balance')

@bp.route('/balance', methods=['GET', 'POST'])
def balance():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    form = BalanceForm()
    if form.validate_on_submit():
        if User.update_balance(current_user.id, form.topup.data, form.withdraw.data):
            flash('We have updated your balance; please check it here.')
            return render_template('balance.html', title='Balance', form=form, your_balance=User.get_balance(current_user.id)), {"Refresh": "1; url="+str(url_for('index.index'))}
        else:
            flash('Oops! Insufficient balance to do this withdrawal :(')            
    return render_template('balance.html', title='Balance', form=form, your_balance=User.get_balance(current_user.id))


##################### The followings are for purchase history ####################
# I just use the following function to split the date variable into year, month, and day:
def Date_Split(early_time, later_time):
    early_y, early_m, early_d = list(map(int, early_time.split("-")))
    later_y, later_m, later_d = list(map(int, later_time.split("-")))
    return [early_y, early_m, early_d], [later_y, later_m, later_d]

# The following function is to filter of purchase history
@bp.route('/purchase_history', methods=['GET', 'POST'])
def purchase_history():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
 
    if request.method == "POST":
        # The followings 5 lines are for input fields to do purchase history filter:
        input_data = request.form
        input_since_date = input_data['since_date']
        input_to_date = input_data['to_date']
        input_seller_fullname = input_data['seller']
        input_seller_name = input_seller_fullname.split() 
        # The following 2 lines are to generate the since_date_2 and to_date_2 which will be used in function get_all_by_uid_since:
        since_date, to_date = Date_Split(input_since_date, input_to_date)
        start_date_2, to_date_2 = datetime.datetime(since_date[0], since_date[1], since_date[2], 0, 0, 0), datetime.datetime(to_date[0], to_date[1], to_date[2], 0, 0, 0)
        # The following 4 lines are to split the Seller's Name the user input into seller_firstname and seller_lastname, seperatively:
        seller_firstname = '%'
        seller_lastname = '%' 
        seller_firstname = '%' + input_seller_name[0] + '%'
        seller_lastname = '%' + input_seller_name[1] + '%'
        
        # The following line is to get the returned value of function get_all_by_uid_since:
            # Note that the returned variable "purchases" will be used in many places later (plz be careful here).
        purchases = Purchase.get_all_by_uid_since(current_user.id, start_date_2, to_date_2, seller_firstname, seller_lastname)
        
        # The following 5 lines are to generate a list which includes all sellers' names of each purchase in each order:
        all_sellers_involves = []
        for p in purchases:
            for s in p.sname:
                if s not in all_sellers_involves:
                    all_sellers_involves.append(s)
    
        return render_template('purchase_history.html', 
                                title='History Of Purchase', 
                                purchase=purchases, 
                                all_sellers_involves=all_sellers_involves, 
                                seller_name_user_input=input_seller_fullname,
                                user_input_since=start_date_2.strftime("%Y-%m-%d"),
                                user_input_to=to_date_2.strftime("%Y-%m-%d"))

    elif request.method == "GET":
        early_limit = datetime.datetime(1980, 9, 14, 0, 0, 0)
        later_limit = datetime.datetime(2050, 9, 14, 0, 0, 0)
        purchases = Purchase.get_all_by_uid_since(current_user.id, early_limit, later_limit)
          
        all_sellers_involves = []
        for p in purchases:
            for s in p.sname:
                if s not in all_sellers_involves:
                    all_sellers_involves.append(s)
        
        early_limit_str = early_limit.strftime("%Y-%m-%d")
        later_limit_str = later_limit.strftime("%Y-%m-%d")

        return render_template('purchase_history.html', 
                                title='History Of Purchase', 
                                purchase=purchases,
                                all_sellers_involves=all_sellers_involves, 
                                seller_name_user_input="",
                                user_input_since=early_limit_str,
                                user_input_to=later_limit_str)


################# The following is for Public View of User #################
@bp.route('/public_view_user/<int:id>')
def public_view_user(id):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    user = User.get(id)
    return render_template('public_view_user.html', title='Public View of This User', user=user)



######################### Celia added some functions for Part 1 above this line (Plz don't get confused) #############################

class SellerRegistrationForm(FlaskForm):
    seller_register =  StringField('Are you willing to become a seller in our website and compile with our policies? (input "y" in the block below to sign up)', 
        validators=[DataRequired()])
    submit = SubmitField('Register')
    #submit = 

    def validate_input(self, seller_register):
        if seller_register.data != "y": 
            raise ValidationError('Invalid Input. To register, input "y" above!')

@bp.route('/seller_register', methods=['GET', 'POST'])
def seller_register():
    form = SellerRegistrationForm()
    is_seller = Seller.is_seller(current_user.id)
    if form.validate_on_submit():
        if form.seller_register.data == "y":
            Seller.seller_register(current_user.id)
            return redirect(url_for('index.index'))
        else:
            flash('Invalid Input. To register, input "y" above!')
            return redirect(url_for('users.seller_register'))
    return render_template('seller_register.html', 
        title='Seller_Register', form=form, is_seller = is_seller)

class SaleForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0, message='Entry must be non-negative!')])
    cate = cate = StringField('Categroy (A, B, C)', validators=[AnyOf(values=['A', 'B','C'])])
    descr = StringField('Description', validators=[DataRequired() , Length(max = 255, message="Do not exceed 255 character")])
    file = FileField('Image',validators=[FileRequired(message="You must up load an image."), FileAllowed(['jpg', 'png'], 'Images only!')])
    number = IntegerField('Number of Items', validators=[DataRequired(), NumberRange(min=0, message='Entry must be non-negative!')])
    submit = SubmitField('Post')

@bp.route('/seller_post', methods=['GET', 'POST'])
def seller_post():
    current_user.is_current_seller = True
    form = SaleForm()
    is_seller = Seller.is_seller(current_user.id)
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path,'../app/static/pic', filename
        ))
        Product2.post_item(form.name.data,
                         form.price.data,
                         form.cate.data,
                         form.descr.data,
                         filename,
                         current_user.id,
                         form.number.data)
        return redirect(url_for('index.index'))        
    return render_template('post_item.html', title='Seller_Post', form=form, is_seller = is_seller)

@bp.route('/selling_history')
def selling_history():
    current_user.is_current_seller = True
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Seller_purchase.get_all_by_seller(current_user.id)
    else:
        avail_history = None
    return render_template('selling_history.html', avail_history = avail_history, is_seller = is_seller)

@bp.route('/items_on_sale')
def items_on_sale():
    current_user.is_current_seller = True
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Product2.items_on_sale(current_user.id)
    else:
        avail_history = None
    return render_template('items_on_sale.html', avail_history = avail_history, is_seller = is_seller)

class InvChangeForm(FlaskForm):
    inv = IntegerField('Number of Items', validators=[DataRequired(), NumberRange(min=0, message='Entry must be non-negative!')])
    submit = SubmitField('Post')

@bp.route('/change_inv/<int:id>', methods = ['GET', 'POST'])
def change_inv(id: int):
    current_user.is_current_seller = True
    form = InvChangeForm()
    if form.validate_on_submit():
        Product.change_inv(id, form.inv.data)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_inv.html', title='change_inv', form=form)

class NameChangeForm(FlaskForm):
    name = StringField('New Name', validators=[DataRequired(), Length(max = 255, message="Do not exceed 255 character")])
    submit = SubmitField('Post')

@bp.route('/change_name/<int:id>', methods = ['GET', 'POST'])
def change_name(id: int):
    current_user.is_current_seller = True
    form = NameChangeForm()
    if form.validate_on_submit():
        Product2.change_name(id, form.name.data)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_name.html', title='change_name', form=form)

class DescrChangeForm(FlaskForm):
    descr = StringField('New Description', validators=[DataRequired() , Length(max = 255, message="Do not exceed 255 character")])
    submit = SubmitField('Post')

@bp.route('/change_descr/<int:id>', methods = ['GET', 'POST'])
def change_descr(id: int):
    current_user.is_current_seller = True
    form = DescrChangeForm()
    if form.validate_on_submit():
        Product2.change_descr(id, form.descr.data)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_descr.html', title='change_descr', form=form)

class CateChangeForm(FlaskForm):
    cate = StringField('New Categroy (A, B, C)', validators=[AnyOf(values=['A', 'B','C'])])
    submit = SubmitField('Post')

@bp.route('/change_cate/<int:id>', methods = ['GET', 'POST'])
def change_cate(id: int):
    current_user.is_current_seller = True
    form = CateChangeForm()
    if form.validate_on_submit():
        Product2.change_cate(id, form.cate.data)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_cate.html', title='change_cate', form=form)

class PriceChangeForm(FlaskForm):
    price = FloatField('New Price', validators=[DataRequired(), NumberRange(min=0, message='Entry must be non-negative!')])
    submit = SubmitField('Post')

@bp.route('/change_price/<int:id>', methods = ['GET', 'POST'])
def change_price(id: int):
    current_user.is_current_seller = True
    form = PriceChangeForm()
    if form.validate_on_submit():
        Product2.change_price(id, form.price.data)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_price.html', title='change_price', form=form)

class ImgChangeForm(FlaskForm):
    file = FileField(validators=[FileRequired(message="You must up load an image."), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')

@bp.route('/change_img/<int:id>', methods = ['GET', 'POST'])
def change_img(id: int):
    current_user.is_current_seller = True
    form = ImgChangeForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path,'../app/static/pic', filename
        ))
        Product2.change_img(id, filename)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_img.html', title='change_img', form=form)

class ProductRemoveForm(FlaskForm):
    ans = StringField('Are you sure you want to delete this product from selling? (input "d" in the block below to delete)', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_input(self, ans):
        if ans.data != "d": 
            raise ValidationError('Invalid Input. To delete, input "d" above!')

@bp.route('/remove_items/<int:id>', methods = ['GET', 'POST'])
def remove_items(id: int):
    current_user.is_current_seller = True
    form = ProductRemoveForm()
    if form.validate_on_submit():
        if form.ans.data == "d":
            Product.product_remove(id)
            return redirect(url_for('users.items_on_sale'))
        else:
            flash('Invalid Input. To delete, input "d" blow!')
            return redirect(url_for('users.remove_items', id = id))
    return render_template('remove_items.html', 
        title='Product_Remove', form=form)

@bp.route('/selling_items_history')
def selling_items_history():
    current_user.is_current_seller = True
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Product.selling_items_history(current_user.id)
    else:
        avail_history = None
    return render_template('selling_items_history.html', avail_history = avail_history, is_seller = is_seller)

@bp.route('/detailed_order/<int:pid>', methods = ['GET', 'POST'])
def detailed_order(pid: int):
    current_user.is_current_seller = True
    p_name = Seller_purchase.get_product_name(pid)
    p_name = list(p_name[0])
    file_name = Seller_purchase.pie_chart(pid)
    runing_low = Seller_purchase.running_low(pid)
    file_name_1 = Seller_purchase.bar_chart(pid)
    running_low_1 =  Seller_purchase.running_low_1(pid)
    file_name_2 = Seller_purchase.line_chart(pid)
    draw = Seller_purchase.draw_line_chart(pid)
    if current_user.is_authenticated:
        avail_history = Seller_purchase.get_all_by_product(pid, current_user.id)
    else:
        avail_history = None
    return render_template('order_details.html', avail_history = avail_history, 
        p_name = p_name[0], file_name = file_name, runing_low = runing_low, file_name_1 = file_name_1, 
        running_low_1 = running_low_1, file_name_2 = file_name_2, draw = draw)

class OrderFulfilledForm(FlaskForm):
    ans = StringField('Are you sure you want to fuifilled this following order? (input "f" in the block below to fulfill)', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_input(self, ans):
        if ans.data != "f": 
            raise ValidationError('Invalid Input. To fulfill this order, input "f" above!')

@bp.route('/fulfilled/<int:id>', methods = ['GET', 'POST'])
def fulfilled(id: int):
    current_user.is_current_seller = True
    form = OrderFulfilledForm()
    avail_history = Seller_purchase.get_all_by_purchaseid(current_user.id, id)
    if form.validate_on_submit():
        if form.ans.data == "f":
            if Seller_purchase.enough_inv(id):
                Seller_purchase.order_fulfill(id, current_user.id)
                return redirect(url_for('users.selling_history'))
            else:
                flash('Not enough inventory for this order. To fulfill this order, please alter the inventory in the items on sale page.')
                return redirect(url_for('users.fulfilled', id = id))
        else:
            flash('Invalid Input. To fulfill this order, input "f" above!')
            return redirect(url_for('users.fulfilled', id = id))
    return render_template('order_fulfilled.html', 
        title='order_fulfilled', form=form, avail_history=avail_history)

@bp.route('/cart/', methods = ['GET', 'POST'])
def cart():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True

    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
    else:
        cart = None
    return render_template('cart.html', cart = cart)

class CartChangeForm(FlaskForm):
    quantity = IntegerField('Number of Items', validators=[DataRequired(), NumberRange(min=1, message='Entry must be positive!')])
    submit = SubmitField('Change')

@bp.route('/addToCart/<int:pid>', methods = ['GET', 'POST'])
def addToCart(pid: int):
    if current_user.is_authenticated:
        if Seller.is_seller(current_user.id):
            current_user.is_current_seller = True
    if current_user.is_authenticated:
        Cart.add_cart(current_user.id, pid)
        return redirect(url_for('users.changeCartQuantity', form=CartChangeForm(), pid=pid))
    else:
        return redirect(url_for('users.login'))
    
@bp.route('/delFromCart/<int:pid>', methods = ['GET', 'POST'])
def delFromCart(pid: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    Cart.delete_cart(current_user.id, pid)
    cart = Cart.get_cart(current_user.id)
    return render_template('cart.html', cart = cart)

@bp.route('/changeCartQuantity/<int:pid>', methods = ['GET', 'POST'])
def changeCartQuantity(pid: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    form = CartChangeForm()
    if form.validate_on_submit():
        Cart.change_cart(current_user.id, pid, quantity=form.quantity.data)
        return redirect(url_for('users.cart'))
    return render_template('cart_quantity.html', form=CartChangeForm(), pid=pid)


@bp.route('/order')
def order():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    if current_user.is_authenticated:
        order_info = Order.get_all_by_user(current_user.id)
    else:
        order_info  = None
    return render_template('order_info.html', order_info = order_info)

@bp.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    # TO DO: redirect to order page
    if Cart.checkout(current_user.id):
        return redirect(url_for('users.order'))
    else:
        return redirect(url_for('users.cart'))


@bp.route('/detailed_order_buyer/<int:order_id>', methods = ['GET', 'POST'])
def detailed_order_buyer(order_id: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    purchase_time = Order.get_purchase_time(order_id)
    total_price = Order.get_total_price(order_id)
    if current_user.is_authenticated:
        order_info = Detailed_Order.get_all_by_oid(order_id)
    else:
        order_info = None
    return render_template('order_details_buyer.html', order_info = order_info, order_id = order_id, purchase_time = purchase_time, total_price = total_price)

class ChatForm(FlaskForm):
    message = StringField('Leave messages to seller', validators=[DataRequired()])
    submit = SubmitField('Send')

@bp.route('/uchats/<int:pur_id>', methods = ['GET', 'POST'])
def uchats(pur_id: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    form = ChatForm()
    msg = Chat.get_all(pur_id)
    order_id = Order.get_order_id(pur_id)
    if form.validate_on_submit():
        Chat.new_message(current_user.id, pur_id, form.message.data)
        return redirect(url_for('users.uchats', pur_id = pur_id))
    return render_template('uchats.html', form=ChatForm(), msg = msg, order_id = order_id)
class ChatForm2(FlaskForm):
    message = StringField('Leave messages to buyer', validators=[DataRequired()])
    submit = SubmitField('Send')

@bp.route('/schatu/<int:pur_id>', methods = ['GET', 'POST'])
def schatu(pur_id: int):
    if Seller.is_seller(current_user.id):
        current_user.is_current_seller = True
    form = ChatForm2()
    msg = Chat.get_all(pur_id)
    if form.validate_on_submit():
        Chat.new_message2(current_user.id, pur_id, form.message.data)
        return redirect(url_for('users.schatu', pur_id = pur_id))
    return render_template('schatu.html', form=ChatForm2(), msg = msg)