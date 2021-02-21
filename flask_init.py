from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:5000/productdb"
mongo = PyMongo(app)

@app.route('/')
def index():
    items = mongo.db.product.find({})
    print ("Items: ", items)
    return render_template("templates/index.html", items=items)

@app.route('/budget')
def moneyUse():
    # return render_template("Graphs.html", )
    return