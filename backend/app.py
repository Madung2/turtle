from datetime import datetime, timedelta
from functools import wraps
import hashlib
from bson import ObjectId
import json
from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
import jwt
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb+srv://test:sparta@cluster0.3puso.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.turtleProject

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})  # 모든 오리진에서 하겠다


# def authorize(f):
#     def decorated_function():
#         if not 'Authorization' in request.headers:
#             abort(401)
#         token = request.headers['Authorization']
#         try:
#             user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         except:
#             abort(401)
#         return f(user)
#     return decorated_function


@app.route("/")
# @authorize
def hello_world(user):
    print(user)
    return jsonify({"message": "success"})


# 리퀘스트 데이터는 비스트링으로 나옴 그래서
# json.load(request.data)형식으로 불러와 써야지 딕셔너리가 됨
# 이메일/패스워드 없을때 에러처리, 이메일 중복시 에러처리
@app.route("/signup", methods=["POST"])
def sign_up():
    data = json.loads(request.data)
    # data = loads(request.data)
    print(data.get("email"))
    print(data["password"])


    pw = data.get('password', None)
    hashed_password = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
        'email': data.get('email'),
        'password': hashed_password
    }
    print(doc)
    user = db.users.insert_one(doc)
    print(doc)
    return jsonify({"message": "success"})


@app.route("/getuserinfo", methods=["GET"])
# @authorize
def get_user_info(user):
    result = db.users.find_one({
        '_id': ObjectId(user["id"])
    })

    return jsonify({"message": "success", "email": result["email"]})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
