import pymongo
from pymongo import MongoClient
from interface import API

client = MongoClient('localhost', 27017)

class MongoDB:
    def insertItem(self, barcode):
        db = client['productdb']
        col = db['product']
        data = API().addItem(barcode)
        # cursor = col.find({'_id': data['_id']}).count()

        if col.find({'_id': data['_id']}).count() > 0:
            col.update({'_id': data['_id']}, {'$inc': {'pQuantity': 1}})
        else:
            doc = col.insert_one(data)