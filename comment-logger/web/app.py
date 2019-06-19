from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)

# connect app to db
client = MongoClient("mongodb://db:27017")

# Set database name
db = client.SentencesDatabase
Users = db["Users"]


# find user in mongo database
def findMongoUser(username):
    return Users.find({"username": username})


# User Authorization function
def verifyPw(user, password):
    hashed_pw = user[0]["password"]
    return bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw


# Number of tokens for user
def getTokens(user):
    return user[0]["tokens"]


# method POST validator
def checkPostedData(request, api):
    data = request.get_json()

    if ("username" not in data) or ("password" not in data):
        return {
            "result": "Missing paramaters: `username` or `password`",
            "status": 301
        }

    if api == "store":
        if "sentence" not in data:
            return {
                "result": "Missing paramater `sentence`",
                "status": 301
            }
        else:
            return {
                "username": data["username"],
                "password": data["password"],
                "sentence": data["sentence"]
            }

    return {"username": data["username"], "password": data["password"]}


class Registration(Resource):
    def post(self):
        data = checkPostedData(request, "registration")
        if "status" in data:
            return jsonify(data)

        username = data["username"]
        password = data["password"]
        current_user = findMongoUser(username)

        # Check if user exists before writing to database
        if current_user.count() == 0:
            Users.insert({
                "username": username,
                "password": bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()),
                "sentences": "",
                "tokens": 10
            })
        else:
            return jsonify({
                "status": 301,
                "message": "This user has already been used"
            })

        return jsonify({
            "status": 200,
            "message": "You successfully signed up for the API"
        })


class Store(Resource):
    def post(self):
        data = checkPostedData(request, "store")

        if "status" in data:
            return jsonify(data)

        username = data["username"]
        password = data["password"]
        sentence = data["sentence"]
        current_user = findMongoUser(username)

        if current_user.count() > 0:
            # Verify username and password
            correct_pw = verifyPw(current_user, password)

            if not correct_pw:
                return jsonify({
                    "status": 302,
                    "message": "Your username or password doesn't match"
                })

            # Verify that the user has enough tokens
            num_tokens = getTokens(current_user)
            if num_tokens <= 0:
                return jsonify({
                    "status": 301,
                    "message": "Tokens are out of date for this user"
                })

            # Write the sentence to the database
            Users.update({
                "username": username
            }, {
                "$set": {
                    "sentence": sentence,
                    "tokens": num_tokens - 1
                }
            })

            return jsonify({
                "status": 200,
                "message": "Your sentence was saved successfully"
            })

        # Username.count() = 0 or password doesn't match
        else:
            return jsonify({
                "status": 302,
                "message": "Your username or password doesn't match"
            })


class Sentence(Resource):
    def post(self):
        data = checkPostedData(request, "sentence")
        if "status" in data:
            return jsonify(data)

        username = data["username"]
        password = data["password"]
        current_user = findMongoUser(username)

        if current_user.count() > 0:
            # Verify username and password
            correct_pw = verifyPw(current_user, password)
            if not correct_pw:
                return jsonify({
                    "status": 302,
                    "message": "Password doesn't match"
                })

            # Verify user has enough tokens
            num_tokens = getTokens(current_user)
            if num_tokens <= 0:
                return jsonify({
                    "status": 301,
                    "message": "Tokens are out of date for this user"
                })

            # Store the sentence
            Users.update({
                "username": username
            }, {
                "$set": {
                    "tokens": num_tokens - 1
                }
            })

            return jsonify({
                "status": 200,
                "message": findMongoUser(username)[0]["sentence"]
            })
        else:
            return jsonify({
                "status": 302,
                "message": "Your username or password doesn't match"
            })


# Register resources for routes
api.add_resource(Registration, "/registration")
api.add_resource(Store, "/store")
api.add_resource(Sentence, "/sentence")


# Default home page for available in 'http://localhost:5000/' of web browswer
@app.route('/')
def hello_world():
    return "Hello World ... !"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
