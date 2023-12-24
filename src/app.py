from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/quick-shop-db-main"


mongo = PyMongo(app)

@app.route('/api/products/all', methods=['GET'])
def get_all_products():
    try:
        products_collection = mongo.db['products']
        data = products_collection.find()
        return dumps(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/products/<id>', methods=['GET'])
def get_product(id):
    print(id)
    try:
        products_collection = mongo.db['products']
        product = products_collection.find_one({"_id": ObjectId(id)})
        if product:
            return dumps(product)
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products/all/categories/<category>', methods=['GET'])
def get_one_category(category):
    try:
        products_collection = mongo.db['products']
        products = products_collection.find({"category": category})

        products_list = list(products)
        if products_list:
            return dumps(products_list)
        else:
            return jsonify({"error": "No products found in this category"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/orders/all', methods=['GET'])
def get_all_orders():
    try:
        orders_collection = mongo.db['orders']
        orders = orders_collection.find()
        orders_list = list(orders)
        if orders_list:
            return dumps(orders_list)
        else:
            return jsonify({"error": "No orders found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/carts', methods=['POST'])
def create_new_cart():
    try:
        carts_collection = mongo.db['carts']
        cart_data = request.json
        result = carts_collection.insert_one(cart_data)
        return jsonify({"success": True, "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route('/api/carts/items', methods=['GET'])
def get_cart_items():
    try:
        carts_collection = mongo.db['carts']
        carts = carts_collection.find()
        carts_list = list(carts)
        if carts_list:
            return dumps(carts_list)
        else:
            return jsonify({"error": "No orders found"}), 404
        return jsonify({"success": True, "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/users/<id>', methods=['GET'])
def get_user_data(id):
    try:
        users_collection = mongo.db['users']
        users = users_collection.find({"id": ObjectId(id)})
        users_list = list(users)
        if users_list:
            return dumps(users_list)
        else:
            return jsonify({"error": "No user found"}), 404
        return jsonify({"success": True, "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

