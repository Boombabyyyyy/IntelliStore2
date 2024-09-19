from flask import Flask, request, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_header, get_jwt_identity
from base64 import b64encode
import sqlite3 as sql
from datetime import datetime
from app import *
from helpers import *
from sqlalchemy import desc

api_blueprint = Blueprint('api', __name__)

# Define data models or structures using fields
product_fields = {
    'product_id': fields.Integer,
    'name': fields.String,
    'price': fields.Integer,
    'unit': fields.String,
    'mfg': fields.String,
    'exp': fields.String,
    'description': fields.String,
    'discount': fields.Float,
    'stock': fields.Integer,
    'category_id': fields.Integer,
    'image': fields.String,
}

class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        products = Products.query.all()
        if products:
            return products
        else:
            abort(404, message="No products found")


    @marshal_with(product_fields)
    @jwt_required()
    def post(self):
        claims = get_jwt()

        product_parser = reqparse.RequestParser()
        # Define parser arguments based on your product structure
        product_parser.add_argument('name', type=str, required=True)
        product_parser.add_argument('price', type=int, required=True)
        product_parser.add_argument('mfg', type=str, required=False)
        product_parser.add_argument('exp', type=str, required=False)
        product_parser.add_argument('description', type=str, required=False)
        product_parser.add_argument('category_id', type=int, required=True)
        product_parser.add_argument('unit', type=str, required=True)
        product_parser.add_argument('stock', type=int, required=True)
        product_parser.add_argument('image', type=str, required=False)
        # Add more arguments as needed

        args = product_parser.parse_args()
        print(args)
        product = {
            'name': args['name'],
            'price': args['price'],
            'unit': args['unit'],
            'mfg': args['mfg'],
            'exp': args['exp'],
            'description': args['description'],
            'stock': args['stock'],
            'category_id': args['category_id'],
            'image': args['image'],
        }
        for key, value in product.items():
            print(f"{key}: {value} - Type: {type(value)}")

        if(claims.get('isadmin') == 1 or claims.get('isadmin') == 2) :
            added_product = add_product(product)

            if added_product:
                return added_product, 201  # 201 Created
            else:
                abort(500, message="Failed to add product")
        else:
            abort(401, message="Access denied, please contact the admin to add this information.")
    
    @jwt_required()
    def delete(self):
        claims = get_jwt()
        product_id = request.get_data(as_text=True)
        product_id = int(product_id)

        if(claims.get('isadmin') == 1 or claims.get('isadmin') == 2):
            return jsonify(delete_product(product_id))
        else:
            abort(401, message="Access denied, please contact the admin to delete this information.")

    
    @marshal_with(product_fields)
    @jwt_required()
    def put(self):
        claims = get_jwt()
        product = request.get_json()
        if(claims.get('isadmin') == 1 or claims.get('isadmin') == 2):
            updated_product = updateproduct(product)
            return updated_product
        else:
            abort(401, message="Access denied, please contact the admin to update this information.")

category_fields = {
    "category_id": fields.Integer,
    "name": fields.String,
    "status": fields.Integer,
}

class CategoryResource(Resource):
    @marshal_with(category_fields)
    def get(self):
        cats = Category.query.filter((Category.status == 1)).all()
        if cats:
            return cats
        else:
            abort(404, message="No products found")

    @jwt_required()
    def post(self):
        claims = get_jwt()
        category = request.get_json()
        user_id = int(claims.get('user_id'))
        if claims.get('isadmin') == 1:
            status = 1
            return add_category(category, status, user_id)
        elif claims.get('isadmin') == 2:
            status = 0
            return add_category(category, status, user_id)
        else:
            abort(401, message="Access denied, please contact the admin to add this information.")
    
    @jwt_required()
    def delete(self):
        claims = get_jwt()
        isadmin =  int(claims.get('isadmin'))
        user_id = int(claims.get('user_id'))
        category_id = request.get_data(as_text=True)
        category_id = int(category_id)
        cat= Category.query.filter((Category.category_id == category_id)).first()

        approvals = Catapprovals.query.filter((Catapprovals.category_id == category_id) & (Catapprovals.status == "pending")).all()

        if approvals:
            abort(400, message="A similar deletion request already exists, please wait for admin approval.")
        if isadmin == 0:
            abort(401, message="Access denied, please contact the admin to delete this information.")
        if not cat:
            abort(400, message="Cannot find category.")
       
        return jsonify(delete_category(category_id, user_id, isadmin, cat.name))
    
    @jwt_required()
    def put(self):
        claims = get_jwt()
        isadmin =  int(claims.get('isadmin'))
        category = request.get_json()
        user_id = int(claims.get('user_id'))

        cat= Category.query.filter((Category.category_id == category["category_id"])).first()

        approvals = Catapprovals.query.filter((Catapprovals.category_id == category["category_id"]) & (Catapprovals.status == "pending")).all()

        if approvals:
            abort(400, message="A similar deletion request already exists, please wait for admin approval.")
        if isadmin == 0:
            abort(401, message="Access denied, please contact the admin to delete this information.")
        if not cat:
            abort(400, message="Cannot find category.")

        if category["name"]:
            return updatecat(category, user_id, isadmin)
        else:
            abort(400, message="Category Name Missing")
        
catapprovals_fields = {
    "approval_id": fields.Integer,
    "user_id": fields.Integer,
    "category_id": fields.Integer,
    "name": fields.String,
    "request_type": fields.Integer,
    "status": fields.String,
}

class CatapprovalsResource(Resource):
    @marshal_with(catapprovals_fields)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        user_id = int(claims.get('user_id'))
        if claims.get('isadmin') == 1:
            approvals = Catapprovals.query.order_by(desc(Catapprovals.approval_id)).all()
            if approvals:
                return approvals, 200
            else:
                return approvals, 400
        elif claims.get('isadmin') == 2:
            approvals = Catapprovals.query.filter(Catapprovals.user_id == user_id).order_by(desc(Catapprovals.approval_id)).all()
            if approvals:
                return approvals, 200
            else:
                return approvals, 400
    
    @jwt_required()
    def put(self):
        data = request.get_json()
        claims = get_jwt()
        if claims.get('isadmin') == 1:
            approval = Catapprovals.query.filter((Catapprovals.approval_id == data["approval_id"]) & (Catapprovals.status == "pending")).first()
            if approval:
                if approval.request_type == 1:
                    return approve_reject_cat_add(approval.category_id, data["approve"], approval.approval_id)
                elif approval.request_type == 3:
                    return approve_reject_cat_del(approval.category_id, data["approve"], approval.approval_id)
                elif approval.request_type == 2:
                    return approve_reject_cat_edit(approval.category_id, data["approve"], approval.approval_id, approval.name)
            else:
                abort(400, message="Invalid approval id, please check.")
        else:
            abort(401, message="Access denied, please contact the admin to approve this request.")


class AddressResource(Resource):
    @jwt_required()
    def post(self):
        
        address = request.get_json()
        user = User.query.filter((User.user_id == address["user_id"])).first()
        if user:
            return add_address(address)
        else:
            abort(400, message="User does not exist")
    
    @jwt_required()
    def put(self):
        user_id = request.get_data(as_text=True)
        user_id = int(user_id)
        return jsonify(get_address(user_id))

class OrderResource(Resource):
    @jwt_required()
    def post(self):
        order = request.get_json()
        return place_order(order)
    
    @jwt_required()
    def get(self):
        claims = get_jwt()
        user_id = claims.get('user_id')
        user_id = int(user_id)
        return jsonify(get_orders(user_id))

user_fields = {
    "user_id": fields.Integer,
    "email": fields.String,
    "mobile": fields.String,
    "firstname": fields.String,
    "lastname": fields.String,
    "password": fields.String,
    "isadmin": fields.String,
    "fs_uniquifier": fields.String,
}

class UserResource(Resource):
    def post(self):
        user = request.get_json()
        return add_user(user)
    
    @marshal_with(user_fields) 
    @jwt_required()  
    def get(self):
        claims = get_jwt()

        if claims.get('isadmin') == 1:
            users = User.query.all()
            if users:
                return users
            else:
                abort(404, message="No Users found")
        else:
            abort(401, message="please contact the admin to access this information.")

class UserByIdResource(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self, user_id):
        claims = get_jwt()

        if claims.get('isadmin') == 1 or claims.get('user_id') == int(user_id):
            user = User.query.filter((User.user_id == user_id)).first()
            if user:
                return user, 200
            else: 
                abort(404, message="User not found")
        else:
            abort(401, message="please contact the admin to access this information.")

login_fields = {
    "message": fields.String,
    "user_id": fields.Integer,
    "tokens": fields.List,
}

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = check_user(data)

        if not user or not check_password_hash(user.password, data["password"]):
            abort(401, message="Invalid username or password!")
        else:
            access_token = create_access_token(identity=user.email, additional_claims={'isadmin': user.isadmin, 'user_id': user.user_id})
            refresh_token = create_refresh_token(identity=user.email, additional_claims={'isadmin': user.isadmin, 'user_id': user.user_id})
            session["user_id"] = user.user_id
            print(user, session["user_id"])
            return {
                    "message": "Logged in successfully",
                    "user_id": user.user_id,
                    "tokens":  [
                        {"access": access_token, "refresh": refresh_token},
                    ]
                }, 200
        
    @jwt_required()
    def get(self):
        claims=get_jwt()
        headers=get_jwt_header()
        return jsonify({"message": "", "headers": headers, "claims": claims})

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        claims=get_jwt()
        
        isadmin = claims.get('isadmin')
        user_id = claims.get('user_id')

        new_access_token = create_access_token(identity=identity, additional_claims={'isadmin': isadmin, 'user_id': user_id})
        new_refresh_token = create_refresh_token(identity=identity, additional_claims={'isadmin': isadmin, 'user_id': user_id})

        return {
                "message": "Token Refreshed successfully",
                "user_id": user_id,
                "tokens":  [
                    {"access": new_access_token, "refresh": new_refresh_token},
                ]
            }, 200


mgr_fields = {
    "user_id": fields.Integer,
    "email": fields.String,
    "mobile": fields.String,
    "firstname": fields.String,
    "lastname": fields.String,
    "status": fields.String,
    "employee_id": fields.String,
}

class MgrResource(Resource):   
    @marshal_with(mgr_fields)
    @jwt_required()   
    def get(self):
        claims = get_jwt()

        if claims.get('isadmin') == 1:
            approvals = Mgrapprovals.query.all()
            if approvals:
                return approvals
            else:
                abort(404, message="No approvals found")
        else: abort(401, message="Unauthorized Access")
    
    @jwt_required()
    def put(self):
        claims = get_jwt()

        if claims.get('isadmin') == 1:
            manager=request.get_json()
            if manager["user_id"]:
                return approvemgr(manager)
            else:
                abort(400, message="User ID Missing")
        else: abort(401, message="Unauthorized Access")

class ProductByIdResource(Resource):
    @marshal_with(product_fields)
    def get(self, product_id):
        product = Products.query.filter((Products.product_id == product_id)).first()
        if product:
            return product, 200
        else: 
            abort(404, message="Product not found")
            
    @jwt_required()
    def put(self, product_id):
        product = request.get_json()
        exists = Products.query.filter((Products.product_id == product_id)).first()
        if exists:
            return updatestock(product)
        else: 
            abort(404, message="Product not found")

class ProductSearchResource(Resource):
    @marshal_with(product_fields)
    def get(self, keyword):
        if keyword.isdigit():
            entered_price = int(keyword)
            min_price = entered_price - 100
            max_price = entered_price + 100
            products = Products.query.filter((Products.price >= min_price) & (Products.price <= max_price)).all()
        else:
            products = Products.query.filter(Products.name.ilike(f"%{keyword}%")).all()
        
        if products:
            return products, 200
        else: 
            abort(404, message="Product not found")

class ProductCategoryResource(Resource):
    @marshal_with(product_fields)
    def get(self, category_id):
        category_id = int(category_id)
        product = Products.query.filter((Products.category_id == category_id)).all()
        if product:
            return product, 200
        else: 
            abort(404, message="Product not found")
cart_fields = {
    "product_id": fields.Integer,
    "qty": fields.Integer,
}
class CartResource(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        user_id = claims.get('user_id')
        data = request.get_json()
        return addtocart(user_id, data)
    
    @marshal_with(cart_fields)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        user_id = claims.get('user_id')
        cart = Cart.query.filter((Cart.user_id == user_id)).all()
        if cart:
                return cart, 200
        else: 
            return [], 200
    
    @jwt_required()
    def delete(self):
        claims = get_jwt()
        user_id = claims.get('user_id')
        product_id = request.get_data(as_text=True)
        return deletecart(user_id, product_id)
    


api = Api(api_blueprint)
api.add_resource(ProductResource, '/product')
api.add_resource(CategoryResource, '/category')
api.add_resource(CatapprovalsResource, '/catapprovals')
api.add_resource(AddressResource, '/address')
api.add_resource(OrderResource, '/order')
api.add_resource(UserResource, '/newuser')
api.add_resource(LoginResource, '/loginuser')
api.add_resource(RefreshResource, '/refresh')
api.add_resource(ProductByIdResource, '/product/<product_id>')
api.add_resource(UserByIdResource, '/user/<user_id>')
api.add_resource(ProductSearchResource, '/product/search/<keyword>')
api.add_resource(ProductCategoryResource, '/product/category/<category_id>')
api.add_resource(MgrResource, '/mgr')
api.add_resource(CartResource, '/cartapi')
