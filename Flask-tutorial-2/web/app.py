#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)

# mongodb://'name in dockerfile':27017
client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users': 0
})


class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set": {'num_of_users': new_num}})
        return str('Hello user ' + str(new_num))


def checkPostedData(postedData, functionName):
    if(functionName == "add" or functionName == 'subtract' or
       functionName == 'multiply'):
        if "x" not in postedData or "y" not in postedData:
            return 301,
        else:
            return 200
    elif(functionName == 'divide'):
        if "x" not in postedData or "y" not in postedData:
            return 301,
        elif int(postedData["y"]) == 0:
            return 302
        else:
            return 200


class Add(Resource):
    # the resource 'Add' was requested using method POST
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "add")
        if(status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x + y

        retMap = {
            "Message": z,
            "Status Code": 200
        }
        return jsonify(retMap)


class Subtract(Resource):
    # the resource 'Subtract' was requested using method POST
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "subtract")
        if(status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x - y

        retMap = {
            "Message": z,
            "Status Code": 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    # the resource 'Multiply' was requested using method POST
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "multiply")
        if(status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = x * y

        retMap = {
            "Message": z,
            "Status Code": 200
        }
        return jsonify(retMap)


class Divide(Resource):
    # the resource 'Divide' was requested using method POST
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "divide")
        if(status_code != 200):
            retJson = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        z = (x*1.0) / y

        retMap = {
            "Message": z,
            "Status Code": 200
        }
        return jsonify(retMap)


api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')
api.add_resource(Visit, '/hello')


@app.route('/')
def hello_world():
    return "Hello World ... !"


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=80)
    app.run(host="0.0.0.0", debug=True)  # docker needs "host"
