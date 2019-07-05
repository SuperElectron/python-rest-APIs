#!/usr/bin/env python
import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient, InsertOne
import bcrypt
import datetime

# instantiate flask application
app = Flask(__name__)
api = Api(app)


# initialize database
def init_db():
    # setup database and db.Users
    # databaseURI = os.getenv('MONGO_DATABASE_URI')
    databaseURI = "mongodb://db:27017"
    client = MongoClient(databaseURI)
    # create database name MoneyMan ...
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
    print(results.inserted_id)


# verify the username exists
def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


# verify correct hashed password
def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


# find money user owns
def cashWithUser(username):
    cash = users.find({"Username": username})[0]["Own"]
    return cash


# find user debt
def debtWithUser(username):
    debt = users.find({"Username": username})[0]["Debt"]
    return debt


# generate http status and message
def generateReturnDictionary(status, msg):
    retJson = {"status": status, "msg": msg}
    return retJson


# verify user exists and password is correct
def verifyCredentials(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False


# makes deposits, transfers, and payments
def updateAccount(username, balance):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Own": balance
        }
    })


# records loan/debt ledger
def updateDebt(username, balance):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Debt": balance
        }
    })


# register a new user.  **BANK** must be first user
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        # check for duplicate username
        if UserExist(username):
            retJson = {
                'status': 301,
                'msg': 'Invalid username, user already exists'
            }
            return jsonify(retJson)

        # create an account with credentials and own/debt ledger
        users.insert({
            "Username": username,
            "Password": bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
            "Own": 0,
            "Debt": 0
        })

        return jsonify(generateReturnDictionary(200, "You successfully signed up for the API"))


# add funds to the user's account
class Add(Resource):
    def post(self, transactionFee=1):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        deposit = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        if deposit <= 0:
            return jsonify(generateReturnDictionary(304, "Must add positive amount"))

        # get and update user ledger
        userBalance = cashWithUser(username)
        deposit -= transactionFee

        # charge transaction fee to user and deposit into BANK's account
        bankBalance = cashWithUser("BANK")
        updateAccount("BANK", bankBalance + transactionFee)

        # add remaining funds to user
        updateAccount(username, userBalance + deposit)

        return jsonify(generateReturnDictionary(200, "Amount Added Successfully to account"))


class Transfer(Resource):
    def post(self, transactionFee=1):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        transfer = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        # get ledgers
        userBalance = cashWithUser(username)
        receiveBalance = cashWithUser(to)
        bankBalance = cashWithUser("BANK")

        # verify user, positive user balance and transfer amount
        if not UserExist(to):
            return jsonify(generateReturnDictionary(301, "Invalid username"))
        if userBalance <= 0:
            return jsonify(generateReturnDictionary(303, "Insufficient funds, please add cash or take a loan"))
        if transfer <= 0:
            return jsonify(generateReturnDictionary(304, "Must transfer a positive amount"))

        # update ledgers
        updateAccount("BANK", bank_cash + transactionFee)
        updateAccount(to, receiveBalance + transfer - transactionFee)
        updateAccount(username, userBalance - transfer)

        return jsonify(generateReturnDictionary(200, "Amount added successfully to account"))


# show the user's balance
class Balance(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        retJson = users.find({
            "Username": username
        }, {
            "Password": 0,  # projections, don't include
            "_id": 0
        })[0]

        return jsonify(retJson)


# give the user a loan
class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        loan = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        if loan <= 0:
            return jsonify(generateReturnDictionary(304, "Must borrow a positive amount"))

        # update ledgers
        balance = cashWithUser(username)
        debt = debtWithUser(username)
        updateAccount(username, balance + loan)
        updateDebt(username, debt + loan)

        return jsonify(generateReturnDictionary(200, "Loan Added to Your Account"))


# pay user loan from user account
class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        payment = postedData["amount"]

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        # get ledger
        balance = cashWithUser(username)
        debt = debtWithUser(username)

        if payment <= 0:
            return jsonify(generateReturnDictionary(304, "Must borrow a positive amount"))
        if balance < payment:
            return jsonify(generateReturnDictionary(303, "Insufficient funds"))

        # update ledger
        updateAccount(username, balance - payment)
        updateDebt(username, debt - payment)

        return jsonify(generateReturnDictionary(200, "Loan Paid"))


# insert restful API resources
api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')


# Default home page for available in 'http://localhost:5000/' of web browswer
@app.route('/')
def hello_world():
    return "Hello World ... !"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
