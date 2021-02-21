import pymongo
from pymongo import MongoClient
from interface import API

client = MongoClient('localhost', 27017)

class MongoDB:
    def insertItem(self, barcode):
        db = client['productdb']
        col = db['product']
        data = API().getItemDetails(barcode)

        if col.find({'pid': data['pid']}).count() > 0:
            col.update({'pid': data['pid']}, {'$inc': {'pQuantity': 1}})
        else:
            doc = col.insert_one(data)

    def doneWithItem(self, barcode):
        db = client['productdb']
        col = db['product']
        budCol = db['budget']
        data = API().getItemDetails(barcode)

        if col.find({'pid': data['pid']}).count() > 0:
            if col.find({'pid': data['pid'], 'pQuantity': 1}).count() > 0:
                col.delete_one({'pid': data['pid']})
                if budCol.find({'pid': data['pid']}).count() > 0:
                    budCol.update({'pid': data['pid']}, {'$inc': {'pQuantity': 1}})
                else:
                    doneData = col.find({'pid': data['pid']}).limit(1).__getitem__(0)
                    doneData['pQuantity'] = 1
                    budCol.insert_one(doneData)
            else:
                col.update({'pid': data['pid']}, {'$inc': {'pQuantity': -1}})
                if budCol.find({'pid': data['pid']}).count() > 0:
                    budCol.update({'pid': data['pid']}, {'$inc': {'pQuantity': 1}})
                else:
                    doneData = col.find({'pid': data['pid']}).limit(1).__getitem__(0)
                    doneData['pQuantity'] = 1
                    budCol.insert_one(doneData)
                # for i in col.find({'pid': data['pid']}):
                #     print(i)

    def cancelItem(self, barcode):
        db = client['productdb']
        col = db['product']
        data = API().getItemDetails(barcode)

        if col.find({'pid': data['pid']}).count() > 0:
            if col.find({'pid': data['pid'], 'pQuantity': 1}).count() > 0:
                col.delete_one({'pid': data['pid']})
            else:
                col.update({'pid': data['pid']}, {'$inc': {'pQuantity': -1}})
                # for i in col.find({'pid': data['pid']}):
                #     print(i)


    def showCollection(self, colName):
        print('\n\nShowing', colName)
        db = client['productdb']
        col = db[colName]
        cursor = col.find({})
        for i in cursor:
            print(i)


    def clearCollection(self, colName):
        db = client['productdb']
        col = db[colName]
        col.delete_many({})