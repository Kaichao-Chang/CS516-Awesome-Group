from cgi import print_exception
from operator import is_
from unicodedata import name
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import BooleanField, PasswordField, StringField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from .models.user import User
from .models.seller import Seller
from .models.product import Product

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
            flash('Invalid email or password')
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
                         form.lastname.data):
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

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
        avail_history = Product.get_all_by_seller(current_user.id)
    else:
        avail_history = None
    # render the page by adding information to the index.html file
    return render_template('selling_history.html', avail_history = avail_history, is_seller = is_seller)

@bp.route('/items_on_sale')
def items_on_sale():
    is_seller = Seller.is_seller(current_user.id)
    if current_user.is_authenticated:
        avail_history = Product.items_on_sale(current_user.id)
    else:
        avail_history = None
    # render the page by adding information to the index.html file
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
            raise ValidationError('Invalid Input. To delete, input "d" blow!')

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

