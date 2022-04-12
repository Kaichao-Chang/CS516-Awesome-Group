from cgi import print_exception
from operator import is_
from unicodedata import name
# from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask import Blueprint, flash, redirect, render_template, request, url_for, flash, Markup, current_app as app, g
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from wtforms import BooleanField, PasswordField, StringField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets.core import HTMLString, html_params, escape
from itsdangerous import URLSafeTimedSerializer

from .models.user import User
from .models.purchase import Purchase
from .models.seller import Seller
from .models.product import Product
from .models.seller_purchase import Seller_purchase

import itertools
import datetime

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



############################################### Update ###############################################
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
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if User.update_password(form.new_pwd.data):
            flash('You have changed your password!')
            return redirect(url_for('users.password'))
    return render_template('change_password.html', title='Password', form=form)
        
       

############# Balance functions to be added in the following #################
#......



@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template("public_view_user.html")


############################### Celia added some functions for Part 1 above this line #################################

class SellerRegistrationForm(FlaskForm):
    seller_register =  StringField('Are you willing to become a seller in our website and compile with our policies? (input "y" in the block below to sign up)', 
        validators=[DataRequired()])
    submit = SubmitField('Register')
    #submit = 

    def validate_input(self, seller_register):
        if seller_register.data != "y": 
            raise ValidationError('Invalid Input. To register, input "y" blow!')

@bp.route('/seller_register', methods=['GET', 'POST'])
def seller_register():
    form = SellerRegistrationForm()
    is_seller = Seller.is_seller(current_user.id)
    if form.validate_on_submit():
        if form.seller_register.data == "y":
            Seller.seller_register(current_user.id)
            return redirect(url_for('index.index'))
        else:
            flash('Invalid Input. To register, input "y" blow!')
            return redirect(url_for('users.seller_register'))
    return render_template('seller_register.html', 
        title='Seller_Register', form=form, is_seller = is_seller)

class SaleForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = DecimalField('Product Price', validators=[DataRequired()])
    number = IntegerField('Number of Items', validators=[DataRequired()])
    submit = SubmitField('Post')

@bp.route('/seller_post', methods=['GET', 'POST'])
def seller_post():
    form = SaleForm()
    is_seller = Seller.is_seller(current_user.id)
    if form.validate_on_submit():
        Product.post_item(form.name.data,
                         form.price.data,
                         current_user.id,
                         form.number.data)
        return redirect(url_for('index.index'))        
    return render_template('post_item.html', title='Seller_Post', form=form, is_seller = is_seller)

@bp.route('/selling_history')
def selling_history():
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Seller_purchase.get_all_by_seller(current_user.id)
    else:
        avail_history = None
    return render_template('selling_history.html', avail_history = avail_history, is_seller = is_seller)

@bp.route('/items_on_sale')
def items_on_sale():
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Product.items_on_sale(current_user.id)
    else:
        avail_history = None
    return render_template('items_on_sale.html', avail_history = avail_history, is_seller = is_seller)

class InvChangeForm(FlaskForm):
    inv = IntegerField('Number of Items', validators=[DataRequired()])
    submit = SubmitField('Post')

@bp.route('/change_inv/<int:id>', methods = ['GET', 'POST'])
def change_inv(id: int):
    form = InvChangeForm()
    if form.validate_on_submit():
        Product.change_inv(id, form.inv.data)
        return redirect(url_for('users.items_on_sale'))        
    return render_template('change_inv.html', title='change_inv', form=form)

class ProductRemoveForm(FlaskForm):
    ans = StringField('Are you sure you want to delete this product from selling? (input "d" in the block below to delete)', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_input(self, ans):
        if ans.data != "d": 
            raise ValidationError('Invalid Input. To delete, input "d" above!')

@bp.route('/remove_items/<int:id>', methods = ['GET', 'POST'])
def remove_items(id: int):
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
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Product.selling_items_history(current_user.id)
    else:
        avail_history = None
    return render_template('selling_items_history.html', avail_history = avail_history, is_seller = is_seller)

@bp.route('/detailed_order/<int:pid>', methods = ['GET', 'POST'])
def detailed_order(pid: int):
    p_name = Seller_purchase.get_product_name(pid)
    p_name = list(p_name[0])
    if current_user.is_authenticated:
        avail_history = Seller_purchase.get_all_by_product(pid, current_user.id)
    else:
        avail_history = None
    return render_template('order_details.html', avail_history = avail_history, p_name = p_name[0])

class OrderFulfilledForm(FlaskForm):
    ans = StringField('Are you sure you want to fuifilled this following order? (input "f" in the block below to fulfill)', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_input(self, ans):
        if ans.data != "f": 
            raise ValidationError('Invalid Input. To fulfill this order, input "f" above!')

@bp.route('/fulfilled/<int:id>', methods = ['GET', 'POST'])
def fulfilled(id: int):
    form = OrderFulfilledForm()
    avail_history = Seller_purchase.get_all_by_purchaseid(current_user.id, id)
    if form.validate_on_submit():
        if form.ans.data == "f":
            if Seller_purchase.enough_inv(id):
                Seller_purchase.order_fulfill(id)
                return redirect(url_for('users.selling_history'))
            else:
                flash('Not enough inventory for this order. To fulfill this order, please alter the inventory in the items on sale page.')
                return redirect(url_for('users.fulfilled', id = id))
        else:
            flash('Invalid Input. To fulfill this order, input "f" blow!')
            return redirect(url_for('users.fulfilled', id = id))
    return render_template('order_fulfilled.html', 
        title='order_fulfilled', form=form, avail_history=avail_history)