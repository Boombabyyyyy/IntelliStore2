import sqlite3 as sql
from flask import Flask, session, render_template, request, g, redirect, flash, jsonify, url_for
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

import requests
import json
import os
from base64 import b64encode
from datetime import datetime
import random
from app import *

# DB Functions for API
def place_order(order):
    date = datetime.now()
    date = date.strftime("%d/%m/%Y %H:%M:%S")
    message={}
    try:
        print(type(order['user_id']))
        con = sql.connect("store.db")
        con.execute("PRAGMA foreign_keys = ON")
        cursor = con.cursor()
        cursor.execute("SELECT order_id FROM Orders ORDER BY order_id DESC LIMIT 1")
        maxappr = cursor.fetchone()
        if maxappr:
            appr_id = maxappr[0]
            appr_id = appr_id+1
        else: appr_id = 1

        user_id = int(order['user_id'])
        status = "Not Yet Dispatched!"
        subtotal = str(order['subtotal'])
        gst = str(order['gst'])
        grandtotal = str(order['grandtotal'])
        shipping = 0
        discount = str(order['discount'])
        address = str(order['address'])
        mobile = str(order['mobile'])
        created_at = str(date)
        payable = str(order['payable'])


        new_order = Orders(order_id=appr_id, user_id=user_id, status=status, subtotal=subtotal, gst=gst, grandtotal=grandtotal, shipping=shipping, discount=discount, address=address, mobile=mobile, created_at=created_at, payable=payable)
        db.session.add(new_order)
        db.session.commit()
        # cursor.execute("INSERT INTO orders (order_id,user_id,created_at,subtotal,gst,grandtotal,discount,address,mobile,payable) VALUES (?,?,?,?,?,?,?,?,?,?)",(appr_id,order['user_id'],str(date),order['subtotal'],order['gst'],order['grandtotal'],order['discount'],order['address'],order['mobile'],order['payable'],))
        # con.commit()

        message["status"] = "successfully placed order"
        return message, 200
    except:
        con.rollback()
        message["status"] = "Failed to place order"
        return message, 400
    finally:
        print(message)
        

def get_orders(user_id):
    orders = []
    try:
        con = sql.connect("store.db")  
        con.row_factory = sql.Row
        cursor=con.cursor()

        cursor.execute("select * from orders where user_id=? ORDER BY order_id DESC",(user_id,))

        rows=cursor.fetchall()
        
        for i in rows:
            order = {}
            order["order_id"] = i["order_id"]
            order["status"] = i["status"]
            order["subtotal"] = i["subtotal"]
            order["gst"] = i["gst"]
            order["grandtotal"] = i["grandtotal"]
            order["discount"] = i["discount"]
            order["address"] = i["address"]
            order["mobile"] = i["mobile"]
            order["created_at"] = i["created_at"]
            order["payable"] = i["payable"]
            orders.append(order)
            
    except:
        orders = []

    return orders

def get_cats():
    cats=[]
    try:
        con = sql.connect("store.db")  
        con.row_factory = sql.Row

        cursor=con.cursor()

        cursor.execute("select * from Category")

        rows=cursor.fetchall()
        for i in rows:
            cat = {}
            cat["category_id"] = i["category_id"]
            cat["name"] = i["name"]
            cats.append(cat)
            
    except:
        cats = []

    return cats


def search_products(keyword):
    products=[]
    try:
        con = sql.connect("store.db")  
        con.row_factory = sql.Row

        cursor=con.cursor()

        cursor.execute("select * from products WHERE name LIKE ?", (keyword,))

        rows=cursor.fetchall()
        for i in rows:
            product = {}
            product["product_id"] = i["product_id"]
            product["name"] = i["name"]
            product["price"] = i["price"]
            product["unit"] = i["Unit"]
            product["mfg"] = i["mfg"]
            product["exp"] = i["exp"]
            product["description"] = i["description"]
            product["discount"] = i["discount"]
            product["stock"] = i["stock"]
            product["category_id"] = i["category_id"]
            product["image"] = i["image"]
            product["image"] = b64encode(product['image']).decode("utf-8")
            products.append(product)
            
    except:
        products = []

    return products

def get_product_by_category(category_id):
    products=[]
    try:
        con = sql.connect("store.db")  
        con.row_factory = sql.Row

        cursor=con.cursor()

        cursor.execute("select * from products WHERE category_id=?", (category_id,))

        rows=cursor.fetchall()
        for i in rows:
            product = {}
            product["product_id"] = i["product_id"]
            product["name"] = i["name"]
            product["price"] = i["price"]
            product["unit"] = i["Unit"]
            product["mfg"] = i["mfg"]
            product["exp"] = i["exp"]
            product["description"] = i["description"]
            product["discount"] = i["discount"]
            product["stock"] = i["stock"]
            product["category_id"] = i["category_id"]
            product["image"] = i["image"]
            product["image"] = b64encode(product['image']).decode("utf-8")
            products.append(product)
            
    except:
        products = []

    return products

def get_address(user_id):
    address_list=[]
    try:
        con = sql.connect("store.db")  
        con.row_factory = sql.Row

        cursor=con.cursor()

        cursor.execute("select * from address where user_id=?",(user_id,))

        rows=cursor.fetchall()
        for i in rows:
            address = {}
            address['address_id'] = i['address_id']
            address['Address'] = i['Address']
            address['mobile'] = i['mobile']
            address_list.append(address)
            
    except:
        address_list = []
    
    return address_list


def get_address_by_id(address_id):
    address={}
    try:
        con = sql.connect("store.db")  
        con.row_factory = sql.Row

        cursor=con.cursor()

        cursor.execute("select * from address where address_id=?",(address_id,))

        i=cursor.fetchone()
        address['address_id'] = i['address_id']
        address['Address'] = i['Address']
        address['mobile'] = i['mobile']
        
            
    except:
        address = {}

    return address

def add_user(user):
    message={}
    try:
        existing_user = User.query.filter((User.email == user["username"])).first()
        if existing_user:
            message["status"] = "Username or email already exists!"
            return message, 400
        
        con = sql.connect("store.db")  
        con.execute("PRAGMA foreign_keys = ON")
        cursor = con.cursor()

        cursor.execute("SELECT user_id FROM user ORDER BY user_id DESC LIMIT 1")

        maxuser = cursor.fetchone()
        user_id1 = maxuser[0]
        user_id1 = user_id1+1
        print(user_id1)

        email=user["username"] 
        mobile=user["mobile"]
        firstname=user["firstname"]
        lastname=user["lastname"]
        isadmin=0
        password=generate_password_hash(user["pw"])
        fs_uniquifier=user["fs_uniquifier"]

        if user["ismgrequest"] == 1:
            employee_id=user["employee_id"]
            new_mgr = Mgrapprovals(user_id=user_id1, email=email, mobile=mobile, firstname=firstname, lastname=lastname, status="pending", employee_id=employee_id)
            db.session.add(new_mgr)
            db.session.commit()

        print(email, mobile, firstname, lastname, password)

        new_user = User(user_id=user_id1, email=email, mobile=mobile, firstname=firstname, lastname=lastname, isadmin=0, password=password, fs_uniquifier=fs_uniquifier)
        db.session.add(new_user)
        db.session.commit()

        # cursor.execute("INSERT INTO user (user_id,firstname,lastname,email,password,mobile) VALUES (?,?,?,?,?,?)", (user_id1,user["firstname"],user["lastname"],user["username"],user["pw"],user["mobile"]))

        # con.commit()

        message["status"] = "User Added successfully"

        print(message["status"])
        return message, 200
    except:
        message["status"] = "Failed to add User"
        return message, 400
    
def check_user(data):
        user = User.query.filter((User.email == data["username"])).first()
        return user

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "token has expired", "error":"token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "signature verification failed", "error":"token_invalid"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "request does not contain a valid token", "error":"authorization_required"}), 401
        
def approvemgr(manager):
    try:
        con =  sql.connect("store.db")
        cursor = con.cursor()
        message={}
        if manager["approve"] == 1:
            cursor.execute("UPDATE Mgrapprovals SET status=? WHERE user_id=?",("Approved", manager["user_id"]))
            cursor.execute("UPDATE User SET isadmin=? WHERE user_id=?",(2, manager["user_id"]))
            con.commit()
            message["status"] = "Manager Approved Sucessfully"
        else:
            cursor.execute("UPDATE Mgrapprovals SET status=? WHERE user_id=?",("Rejected", manager["user_id"]))
            cursor.execute("UPDATE User SET isadmin=? WHERE user_id=?",(0, manager["user_id"]))
            con.commit()
            message["status"] = "Manager Rejected"
        
        print(message["status"])

        return message, 200
    except:
        msg=" Error, couldn't update Manager"
        print(msg)
        return message, 400

    finally:
        con.close()

def add_product(product):
    print(product)
    try:
        
        with sql.connect('store.db') as con:
            con.execute("PRAGMA foreign_keys = ON")
            
            cursor = con.cursor()

            # cursor.execute("SELECT product_id FROM Products ORDER BY product_id DESC LIMIT 1")

            # maxprod = cursor.fetchone()
            # prod_id = maxprod[0]
            # prod_id = prod_id+1

            cursor.execute("INSERT INTO Products (name,price,mfg,exp,description,category_id,Unit,stock,image) VALUES (?,?,?,?,?,?,?,?,?)", (product['name'],product['price'],product['mfg'],product['exp'],product['description'],product["category_id"],product["unit"],product["stock"],product["image"],))

            con.commit()

            msg = "Product Successfully Added"

            print(msg)

    except:
        con.rollback()
        msg="Error, couldn't add product"
        flash(msg)
    finally:
        con.close()
        return product
    
def updateproduct(product):
    try:
        con =  sql.connect("store.db")
        cursor = con.cursor()
        cursor.execute("UPDATE Products SET name=?,price=?,stock=?,mfg=?,exp=?,description=?,category_id=?,unit=?,image=? WHERE product_id=?",(product['name'],product['price'], product['stock'],product['mfg'],product['exp'],product['description'],product["category_id"],product['unit'], product['image'],product['product_id'],))
        con.commit()
        
        msg = "Product updated Sucessfully"
        print(msg)

    except:
        msg="Error, couldn't update product"
        con.rollback()
        print(msg)
        return msg, 400

    finally:
        con.close()
        return product, 200
        
def updatestock(product):
    msg={}
    try:
        product_id = product['product_id']
        stock = product['stock']
        print(product_id,stock)
        con =  sql.connect("store.db")
        cursor = con.cursor()
        cursor.execute("UPDATE Products SET stock=? WHERE product_id=?",(stock,product_id))
        con.commit()
        
        msg["status"] = "Product Stock updated Sucessfully"
        print(msg)
        return msg, 200

    except:
        msg["status"]="Error, couldn't update stock"
        print(msg)
        return msg, 400
    
    finally:
        con.close()

def add_address(address):
    print(address)
    try:
        with sql.connect('store.db') as con:
            con.execute("PRAGMA foreign_keys = ON")

            cursor = con.cursor()

            cursor.execute("INSERT INTO address (user_id, Address, mobile) VALUES (?,?,?)", (address['user_id'],address['address'],address['mobile'],))

            con.commit()

            msg = "Address Successfully Added"

            print(msg)

    except:
        con.rollback()
        msg="Error, couldn't add address"
        return msg, 400
    finally:
        con.close()
        print(msg)
        return msg, 200

def add_category(category, status, user_id):
    try:
        with sql.connect('store.db') as con:

            cursor = con.cursor()

            cursor.execute("SELECT category_id FROM Category ORDER BY category_id DESC LIMIT 1")

            maxcat = cursor.fetchone()
            cat_id = maxcat[0]
            cat_id = cat_id+1
            cursor.execute("INSERT INTO Category (category_id, name, status) VALUES (?,?,?)", (cat_id, category['name'], status,))

            if status == 1:
                msg = "Category Successfully Added"
            elif status == 0:
                cursor.execute("SELECT approval_id FROM Catapprovals ORDER BY approval_id DESC LIMIT 1")
                maxappr = cursor.fetchone()
                if maxappr:
                    appr_id = maxappr[0]
                    appr_id = appr_id+1
                else: appr_id = 1
                cursor.execute("INSERT INTO Catapprovals (approval_id, user_id, category_id, name, request_type, status) VALUES (?,?,?,?,?,?)", (appr_id, user_id, cat_id, category['name'], 1, "pending",))
                msg = "Category Successfully sent to admin for approval"
            con.commit()

            print(msg)
            return msg, 200

    except:
        con.rollback()
        msg="Error, couldn't add catrgory"
        flash(msg)
        return msg, 400
    finally:
        con.close()

def updatecat(category, user_id, isadmin):
    try:
        con =  sql.connect("store.db")
        cursor = con.cursor()
        category_id = category['category_id']
        name = category['name']

        if isadmin == 1:
            cursor.execute("UPDATE Category SET name=? WHERE category_id=?",(name, category_id,))
            msg = " Category updated Sucessfully"
            print(msg)
        elif isadmin == 2:
             cursor.execute("SELECT approval_id FROM Catapprovals ORDER BY approval_id DESC LIMIT 1")
             maxappr = cursor.fetchone()
             if maxappr:
                appr_id = maxappr[0]
                appr_id = appr_id+1
             else: appr_id = 1
             cursor.execute("INSERT INTO Catapprovals (approval_id, user_id, category_id, name, request_type, status) VALUES (?,?,?,?,?,?)", (appr_id, user_id, category_id, name, 2, "pending",))
             msg = "Category Updation Successfully sent to admin for approval"

        con.commit()

        return msg, 200
    except:
        msg=" Error, couldn't update Category"
        print(msg)
        return msg, 400

    finally:
        con.close()
        
def approve_reject_cat_add(category_id, approve, approval_id):
    try:
        con =  sql.connect("store.db")
        cursor = con.cursor()
        if approve == 1:
            cursor.execute("UPDATE Category SET status=? WHERE category_id=?",(1 , category_id))
            cursor.execute("UPDATE Catapprovals SET status=? WHERE approval_id=?",("approved" , approval_id))
            msg = " Category approved and added Sucessfully"
        elif approve == 0:
            con.execute("DELETE from category WHERE category_id = ?",(category_id,))
            cursor.execute("UPDATE Catapprovals SET status=? WHERE approval_id=?",("rejected" , approval_id))
            msg = " Category rejected and deleted Sucessfully"
        con.commit()
        
        
        print(msg)

        return msg, 200
    except:
        msg=" Error, couldn't approve and add Category"
        print(msg)
        return msg, 400

    finally:
        con.close()

def approve_reject_cat_edit(category_id, approve, approval_id, name):
    try:
        con =  sql.connect("store.db")
        cursor = con.cursor()
        if approve == 1:
            cursor.execute("UPDATE Category SET name=? WHERE category_id=?",(name , category_id))
            cursor.execute("UPDATE Catapprovals SET status=? WHERE approval_id=?",("approved" , approval_id))
            msg = " Category updation approved and updated Sucessfully"
        elif approve == 0:
            cursor.execute("UPDATE Catapprovals SET status=? WHERE approval_id=?",("rejected" , approval_id))
            msg = " Category updation rejected, no changes made to category"
        con.commit()
    
        print(msg)

        return msg, 200
    except:
        msg=" Error, couldn't approve and add Category"
        print(msg)
        return msg, 400

    finally:
        con.close()

def approve_reject_cat_del(category_id, approve, approval_id):
    try:
        con =  sql.connect("store.db")
        cursor = con.cursor()
        if approve == 1:
            con.execute("DELETE from category WHERE category_id = ?",(category_id,))
            con.execute("DELETE from products WHERE category_id = ?",(category_id,))
            cursor.execute("UPDATE Catapprovals SET status=? WHERE approval_id=?",("approved" , approval_id))
            msg = " Category deletion approved and deleleted Sucessfully"
        elif approve == 0:
            cursor.execute("UPDATE Catapprovals SET status=? WHERE approval_id=?",("rejected" , approval_id))
            msg = " Category deletion rejected"
        con.commit()
        
        
        print(msg)

        return msg, 200
    except:
        msg=" Error, couldn't approve and delete Category"
        print(msg)
        return msg, 400

    finally:
        con.close()

def addtocart(user_id, data):
    msg=""
    product_id = data['product_id']
    qty=int(data['qty'])
    con =  sql.connect("store.db")
    cursor = con.cursor()

    inCartCheck=Cart.query.filter((Cart.user_id==user_id) & (Cart.product_id==product_id)).first()
    cursor.execute("SELECT stock FROM Products WHERE product_id=?",(product_id))
    result = cursor.fetchone()
    stock = int(result[0])

    
    if(inCartCheck):
        currentQty=inCartCheck.qty 
        newQty = currentQty + qty
        print(currentQty, stock)
        if currentQty == stock:
            msg="no more stock available :( , maximum quantitiy in cart"
        elif newQty <= stock:
            cursor.execute("UPDATE cart SET qty=? WHERE user_id=? AND product_id=?",(newQty,user_id,product_id))
            con.commit()
            # Cart.query.filter((Cart.user_id == user_id) & (Cart.product_id == product_id)).update({"qty": newQty})
            msg="additional quantities added successfully"
        else:
            msg="not enough stock available! :("
    else:
        if qty <= stock:
            cursor.execute("INSERT INTO cart (user_id,product_id,qty,category_id) VALUES (?,?,?,?)",(user_id,product_id,qty,1))
            con.commit()
            msg="successfully added to cart"
        else:
            cursor.execute("INSERT INTO cart (user_id,product_id,qty,category_id) VALUES (?,?,?,?)",(user_id,product_id,stock,1))
            con.commit()

    return msg, 200

def deletecart(user_id, product_id):
    con =  sql.connect("store.db")
    try:
        cursor = con.cursor()
        con.execute("DELETE FROM cart WHERE user_id=? AND product_id=?", (user_id, product_id))
        con.commit()
        msg="successfully delted"
        return msg, 200

    except:
        con.rollback()
        msg="failed to delete"
        return msg, 400
    finally:
        con.close()

def delete_product(product_id):
    message={}
    try: 
        product_id=int(product_id)
        con = sql.connect("store.db")
        cursor = con.cursor()
        con.execute("DELETE from products WHERE product_id = ?",(product_id,))
        con.execute("DELETE from cart WHERE product_id = ?",(product_id,))
        con.commit()
        message["status"] = "Product deleted successfully"
    except:
        con.rollback()
        message["status"] = "Cannot delete Product"
    finally:
        con.close()

    return message

def delete_category(category_id, user_id, isadmin, name):
    message={}
    try: 
        con = sql.connect("store.db")
        cursor = con.cursor()

        if isadmin == 1:
            con.execute("DELETE from category WHERE category_id = ?",(category_id,))
            con.execute("DELETE from products WHERE category_id = ?",(category_id,))
            message["status"] = "Category deleted successfully"
        elif isadmin == 2:
            cursor.execute("SELECT approval_id FROM Catapprovals ORDER BY approval_id DESC LIMIT 1")
            maxappr = cursor.fetchone()
            if maxappr:
                appr_id = maxappr[0]
                appr_id = appr_id+1
            else: appr_id = 1
            cursor.execute("INSERT INTO Catapprovals (approval_id, user_id, category_id, name, request_type, status) VALUES (?,?,?,?,?,?)", (appr_id, user_id, category_id, name, 3, "pending",))
            message["status"] = "Category Deletion Successfully sent to admin for approval"


        con.commit()
        return message, 200
        
    except:
        con.rollback()
        message["status"] = "Cannot delete category"
        return message, 400
    
    finally:
        con.close()

    

def get_product_by_id(product_id):
    product = {}
    try:
        con = sql.connect("store.db")
        con.row_factory = sql.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", 
                       (product_id,))
        i = cursor.fetchone()
        product["product_id"] = i["product_id"]
        product["name"] = i["name"]
        product["price"] = i["price"]
        product["unit"] = i["Unit"]
        product["mfg"] = i["mfg"]
        product["exp"] = i["exp"]
        product["description"] = i["description"]
        product["discount"] = i["discount"]
        product["stock"] = i["stock"]
        product["category_id"] = i["category_id"]
        product["image"] = i["image"]
        product["image"] = b64encode(product['image']).decode("utf-8")
    except:
        product={}
    
    return product