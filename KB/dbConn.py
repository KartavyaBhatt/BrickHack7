import pymongo
from pymongo import MongoClient
from interface import API

client = MongoClient()
client = MongoClient('localhost', 27017)

# Debugging
# db = client['productdb']
# col = db['product']
# col.delete_many({})

class MongoDB:
    def insertItem(self, barcode):
        db = client['productdb']
        col = db['product']
        doc = col.insert_one(API().addItem(barcode))
