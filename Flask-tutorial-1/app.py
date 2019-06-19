from flask import Flask, jsonify, request

# app = Flask("hi")
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World ... !"


@app.route('/info')
def info():
    return "This is the info page"


@app.route('/add_two_nums', methods=["POST"])
def add_two_nums():
    # Get x,y from the posted data
    dataDict = request.get_json()

    if 'x' not in dataDict:
        return "ERROR", 305
    if 'y' not in dataDict:
        return "ERROR", 305

    x = dataDict["x"]
    y = dataDict["y"]
    z = x + y
    retJSON = {
        "z": z
    }
    return jsonify(retJSON), 200


@app.route('/about')
def bye():
    # API returns Json, so this is out first setup with it.
    retJson = {
        'field1': 'abc',
        'field2': 'def'
    }

    return jsonify(retJson)

if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=80)
    app.run(debug=True)  # this gives live debugging updates in command line
