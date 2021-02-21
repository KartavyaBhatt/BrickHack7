import pymongo
from pymongo import MongoClient
from interface import API

client = MongoClient('localhost', 27017)

class MongoDB:
    def insertItem(self, barcode):
        db = client['productdb']
        col = db['product']
        data = API().getItemDetails(barcode)

        if col.find({'_id': data['_id']}).count() > 0:
            col.update({'_id': data['_id']}, {'$inc': {'pQuantity': 1}})
        else:
            doc = col.insert_one(data)

    def doneWithItem(self, barcode):
        db = client['productdb']
        col = db['product']
        data = API().getItemDetails(barcode)

        if col.find({'_id': data['_id']}).count() > 0:
            if col.find({'_id': data['_id'], 'pQuantity': 1}).count() > 0:
                col.delete_one({'_id': data['_id']})
            else:
                col.update({'_id': data['_id']}, {'$inc': {'pQuantity': -1}})
                for i in col.find({'_id': data['_id']}):
                    print(i)