import sqlite3 as sql
from flask import Flask, session, render_template, request, g, redirect, flash, jsonify, url_for, Response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from celery import Celery
from flask_caching import Cache
from celery.schedules import crontab
from celery.signals import celeryd_after_setup
import requests
import json
import os
from base64 import b64encode
from datetime import datetime
from celery_config import make_celery
import random
import yaml
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "store.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey' 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['FLASK_JWT_SECRET_KEY'] = "79775734289930888957"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Update with your Redis server information
app.config['result_backend'] = 'redis://localhost:6379/0'

db = SQLAlchemy(app)
jwt = JWTManager()

jwt.init_app(app)

app.config['CACHE_TYPE'] = 'simple'  # Use an in-memory cache for simplicity
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds (5 minutes)
cache = Cache(app)

celery = make_celery(app)


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    status =  db.Column(db.Integer, default=0, nullable=True) # 0 for pending, 1 for approved

class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False) 
    price = db.Column(db.Numeric, nullable=False)
    mfg = db.Column(db.String(255))  
    exp = db.Column(db.String(255))  
    description = db.Column(db.Text)
    discount = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))  # Foreign key to Category table
    image = db.Column(db.String(50000))
    unit = db.Column(db.String(255), default='Rs/unit', nullable=False)  
    stock = db.Column(db.Integer, default=1, nullable=False)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)  
    mobile = db.Column(db.String(255))  
    firstname = db.Column(db.String(255), nullable=False) 
    lastname = db.Column(db.String(255)) 
    password = db.Column(db.String(255), nullable=False) 
    isadmin = db.Column(db.Integer, default=0, nullable=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  

class Mgrapprovals(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)  
    mobile = db.Column(db.String(255))  
    firstname = db.Column(db.String(255), nullable=False) 
    lastname = db.Column(db.String(255)) 
    status =  db.Column(db.String(255), nullable=False)
    employee_id = db.Column(db.String(255), nullable=False)

class Catapprovals(db.Model):
    approval_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) # Foreign key to User table
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)  # Foreign key to Category table
    name = db.Column(db.String(100), nullable=True)
    request_type = db.Column(db.Integer, default=0, nullable=False) # 1 for add, 2 for update and 3 for delete.
    status =  db.Column(db.String(255), nullable=False)


class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True, unique=True)
    role = db.Column(db.String(255), unique=True, nullable=False)

class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign key to User table
    address = db.Column(db.Text)
    mobile = db.Column(db.String(255), nullable=False) 

class Cart(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)  # Foreign key to User table
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True, nullable=False)  # Foreign key to Products table
    qty = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)  # Foreign key to Category table

    # Define the unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_cart_item'),
    )

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign key to User table
    status = db.Column(db.String(255), default='Not Yet Dispatched', nullable=True) 
    subtotal = db.Column(db.String(255), nullable=False)  
    gst = db.Column(db.String(255), nullable=False)  
    grandtotal = db.Column(db.String(255), nullable=False)  
    shipping = db.Column(db.Numeric, default=0, nullable=True)
    discount = db.Column(db.String(255), nullable=True)  
    address = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(255), nullable=False)  
    created_at = db.Column(db.String(255), nullable=False)  
    payable = db.Column(db.String(255), nullable=False)  

class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True, nullable=False)  # Foreign key to orders table
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), primary_key=True, nullable=False)  # Foreign key to Products table
    quantity = db.Column(db.Integer, nullable=False)

    # Define the unique constraint
    __table_args__ = (
        db.UniqueConstraint('order_id', 'product_id', name='unique_order_item'),
    )

def create_tables():
    with app.app_context():
        # if app.debug:
        #     db.drop_all()
        try:
            db.create_all()
            pw=str(generate_password_hash("admin1234"))
            print("Tables created successfully!")
            with sql.connect('store.db') as con:
                con.execute("PRAGMA foreign_keys = ON")
                cursor = con.cursor()
                cursor.execute("INSERT INTO user (user_id,firstname,lastname,email,password,mobile,isadmin,fs_uniquifier) VALUES (?,?,?,?,?,?,?,?)", (1,"John","Reese","admin@itstore.in",pw,"9930888957",1,"alskdjfhg"))
                cursor.execute("INSERT INTO Category (category_id, name, status) VALUES (?,?,?)", (1, "Beverages", 1))
                cursor.execute("INSERT INTO Products (product_id,name,price,mfg,exp,description,category_id,Unit,stock, image) VALUES (?,?,?,?,?,?,?,?,?,?)", (1,"Nimbooz",20,"01/10/23","01/10/23","Freshness overloaded",1,"Rs/unit", 10, "/9j/4AAQSkZJRgABAQEAeAB4AAD/2wBDAFA3PEY8MlBGQUZaVVBfeMiCeG5uePWvuZHI////////////////////////////////////////////////////2wBDAVVaWnhpeOuCguv/////////////////////////////////////////////////////////////////////////wgARCAEYARgDASIAAhEBAxEB/8QAGAABAQEBAQAAAAAAAAAAAAAAAAIDAQT/xAAWAQEBAQAAAAAAAAAAAAAAAAAAAQL/2gAMAwEAAhADEAAAAdgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADNNHmHpYalBQAAAAAAAAAAAAAGWuaZLJO0WUGgAAAAAAAAAAAAAHHDriO95woUAAAAAAAAAAAAAOEiAO9noqaoAAAAAAAAAAAABNScEDpzvOnKmjooAAAAAAAAAAABzohKSkiuwKvPRQoAAAAAAAAAAABNQZUrOeKSzy+VG2WtdFoAAAAAAAAAAADnRjcdyoSnURrlruBQAAAAAAAAAAAAGOmemL3idSk1mxrnpqBQAAAAAAAAAAAAGWmd4dmp05SZWmWtgUAAAAAAAAAAAAOGVRUlcdWe1zKdctdAoAAAAAAAAAAABF5I7Pcq7KUcs5rjpVi0AAAAAAAAAAABnoMWiSFCFjPVVAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH//xAAgEAABAgcBAQEAAAAAAAAAAAABAEACEBEgMUFQcDAS/9oACAEBAAEFAvPorBh9FZDh9EFRflUQ8GPDPDPDPEqqqqqqqqDw8OLFxQw6OBcX9LN8Lb8oS283LctvN2jL3dm39H8VpmHcXwhw6i+Ax6//AP/EABoRAQACAwEAAAAAAAAAAAAAABEAQAFQYBD/2gAIAQMBAT8B1jGljh2NEh1R4b//xAAZEQADAQEBAAAAAAAAAAAAAAAAAUARYHD/2gAIAQIBAT8B8Y02NQsUSh0XRf/EABQQAQAAAAAAAAAAAAAAAAAAAKD/2gAIAQEABj8CGT//xAAiEAACAQQCAgMBAAAAAAAAAAAAAREQITFAIFBBUWFwgXH/2gAIAQEAAT8h+vnrPQWfRjGyZImWrfZfoW4JJJJJ3vPJbmHVljoyxt4dI7ookSJEhpe48IRBBBBBhyK63Bc2DbycEi3yxVCq90sipaBYp47qyIj3c9ESWWMW7WVXkO7hDFu1kIklR/SysOWvW8KhtLI3K/SGyPYsdx4IsfI1P7wedxrQLg/ijGlbeaFWavcEbwQ6Twh+j3bkUgggj6//AP/aAAwDAQACAAMAAAAQ88888888888888888888888888888888888888888885EU888888888888888p0h888888888888888wGG08888888888888oW+OQ88888888888888W6q+8888888888888oTzjq888888888888883DUT8888888888888otG2F8888888888888oGVU088888888888888nnQe8888888888888sdAiw88888888888889OeFu8888888888888Yatu58888888888888888888888888888888888888888888888888888888888888/8QAHBEBAAICAwEAAAAAAAAAAAAAAQAREEAwMVBg/9oACAEDAQE/EPLcC2g9SmBv4ayUlNCsgVzhl0AuVWiNRdKudgwYsHQVgFe9/8QAHhEAAgEFAAMAAAAAAAAAAAAAAAERITAxQEEQYHD/2gAIAQIBAT8Q+Lt+RO+1JCO6B1oIQwvvJwakwvwSkS0DIEhaEegf/8QAJRABAAICAQQCAgMBAAAAAAAAAQARITFAQVFhcRAgcKFQgZHB/9oACAEBAAE/EPw5cs/gUKBS5fdgwRpYlC8/X6lMpgNTRzwaaCHeJ5CVdSBoefpP6EtjddGGufrs9fiW6Sw5g2XzFom7fQiWRU8xaQ+ox3cGw5ZWntD7M0cvph9nmgX9ncNHLSyUMGpftPAT0T0T1S+HHMt3r0gvMPqBsBsioe5yzbhgSpUqJBi5+hyzfo+ARQ+CslTJqGDluRlGjC0ogusC3uABiViaPfMdTOkBWIU3eJYSU1CmW46hnmiVnn4BFX4eI2q6dxZbL6TSa+aP9IajnEQI+iYOgys0mrm/sTSULVwSzMsUL6bq4qRl1mBFvmOogberFQboLqNXZ8TFayP1FCN33g6tZ6hMeYOm+JZAbuXZ0IVF/wC0B1zWYtFsWOC9nmVd5nR4gGfMGbmgbmiprKF5d/FFiX8W7zrcWOX35dQDHWAdGF9mAO8uXG+zF+qFCDJy0slpT2npPSekt2gMCj8e/wD/2Q=="))
                cursor.execute("INSERT INTO Roles (role_id, role) VALUES (?,?)", (0, "User"))
                cursor.execute("INSERT INTO Roles (role_id, role) VALUES (?,?)", (1, "Super Admin"))
                cursor.execute("INSERT INTO Roles (role_id, role) VALUES (?,?)", (2, "Store Manager"))
                con.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")

create_tables()

@celeryd_after_setup.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule the task to run daily in the evening (you can adjust the time)
    print("started")
    sender.add_periodic_task(crontab(hour=16, minute=26), check_user_activity.s())
    print("done")

@celery.task
def check_user_activity():
    # Your logic to check if the user has not visited/bought anything
    # Send reminders via Google Chat webhook, SMS, or Email accordingly
    # Implement the necessary functions or use external libraries for sending messages
    print("user activity checked")
    send_reminder_google_chat.delay()
    
    # You can add other reminder functions as needed

@celery.task
def send_reminder_google_chat():
    print("sendMessage started")
    # Replace these placeholders with your actual values
    chat_webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAoCdHBEs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=d_uy02klGQ90qlSQ42c6bnvhRbuFmfNwEOWqus8iE8k'
    room_name = 'IntelliStore Updates'
    
    # Message content
    message = {
        'text': 'Don\'t forget to visit/buy something today from intellistore!',
    }

    # Google Chat API payload
    payload = {
        'text': message,
    }

    # Make the POST request to the Google Chat API
    response = requests.post(chat_webhook_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print('Reminder sent successfully!')
    else:
        print(f'Failed to send reminder. Status code: {response.status_code}, Response: {response.text}')

# Page Routes
@app.route('/')
def serve_yaml():
    # Replace 'your_file.yaml' with the path to your YAML file
    file_path = 'Intellistore.yaml'

    # Read the YAML file
    with open(file_path, 'r') as file:
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)

    # Render the YAML data in an HTML template
    return render_template('yaml_template.html', yaml_data=yaml_data)


#<!------------------------- Api ------------------------->

from api import api_blueprint
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run() #run app