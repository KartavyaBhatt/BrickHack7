# from sshtunnel import SSHTunnelForwarder

from flask import Flask, render_template
from flask_pymongo import PyMongo

# server = SSHTunnelForwarder("192.168.0.21", "productdb", remote_bind_address=('127.0.0.1', 5000))

# server.start()

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/productdb"
mongo = PyMongo(app)

@app.route('/')
def index():
    items = mongo.db.product.find({})
    first_item = mongo.db.product.find().sort("_id", -1).limit(1).__getitem__(0)
    return render_template("index.html", items=items, first_item=first_item)

# server.stop();