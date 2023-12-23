from flask import Flask, jsonify
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


if __name__ == '__main__':
    app.run(debug=True)

