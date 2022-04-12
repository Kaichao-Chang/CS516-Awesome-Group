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
from .models.seller_purchase import Seller_purchase

bp = Blueprint('users_2', __name__)


