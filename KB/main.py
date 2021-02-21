from dbConn import MongoDB

db = MongoDB()

db.clearCollection('product')
db.clearCollection('budget')

db.insertItem("07789044383")
db.insertItem("07789044383")
db.insertItem("07789044383")
db.insertItem("07789044383")
db.insertItem("07789033846")
db.insertItem("72225216105")
db.insertItem("07789042174")
db.insertItem("07789035925")
db.insertItem("07789017428")

# db.showCollection('product')

db.doneWithItem("07789044383")
db.doneWithItem("07789044383")
db.doneWithItem("07789044383")

# db.showCollection('budget')
# db.showCollection('product')

# print(db.totalExpense('product'))
# print(db.totalExpense('budget'))