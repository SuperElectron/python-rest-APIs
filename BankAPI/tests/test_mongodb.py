from pymongo import MongoClient
import bcrypt
import datetime
from pprint import pprint

# connect to Mongo database
databaseURI = "mongodb://db:27017"
client = MongoClient(databaseURI)
db = client.MoneyManagementDB
users = db["Users"]

bankPassword = "123abc"
firstEntry = {
    "Username": "BANK",
    "Password": bcrypt.hashpw(bankPassword.encode('utf8'), bcrypt.gensalt()),
    "Own": 0,
    "Debt": 0,
    "date": datetime.datetime.utcnow()
}

results = users.insert_one(firstEntry)


# Issue the serverStatus command and print the results
# serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)
