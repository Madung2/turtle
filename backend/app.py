from datetime import datetime, timedelta
from functools import wraps
import hashlib
from bson import ObjectId
import json
from flask import Flask, abort, jsonify, request, Response
from flask_cors import CORS
import jwt
from pymongo import MongoClient

SECRET_KEY = 'TURTLE'

client = MongoClient('localhost', 27017)
db = client.turtleProject

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})  # 모든 오리진에서 하겠다


def authorize(f):
    @wraps(f)
    def decorated_function():
        if not 'Authorization' in request.headers:
            abort(401)
        token = request.headers['Authorization']
        try:
            user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            abort(401)
        return f(user)
    return decorated_function


@app.route("/")
@authorize
def hello_world(user):

    return jsonify({"message": "success"})


# 리퀘스트 데이터는 비스트링으로 나옴 그래서
# json.load(request.data)형식으로 불러와 써야지 딕셔너리가 됨
# 이메일/패스워드 없을때 에러처리, 이메일 중복시 에러처리
@app.route("/signup", methods=["POST"])
def sign_up():
    data = json.loads(request.data)
    # data = loads(request.data)

    pw = data.get('password', None)
    hashed_password = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    doc = {
        'email': data.get('email'),
        'password': hashed_password
    }

    user = db.users.insert_one(doc)

    return jsonify({"status": "success"})


@app.route("/login", methods=["POST"])
def login():
    print(request)
    data = json.loads(request.data)
    print(data)

    email = data.get("email")
    password = data.get("password")
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(hashed_pw)
    result = db.users.find_one({
        'email': email,
        'password': hashed_pw
    })
    print(result)
    if result is None:
        return jsonify({"message": "아이디나 비밀번호가 옳지 않습니다."}), 401

    payload = {
        'id': str(result["_id"]),
        'exp': datetime.utcnow() + timedelta(seconds=60*60*24)  # 로그인 24시간 유지
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print(token)

    return jsonify({"message": "success", "token": token})


@app.route("/getuserinfo", methods=["GET"])
@authorize
def get_user_info(user):

    result = db.users.find_one({
        '_id': ObjectId(user["id"])
    })

    return jsonify({"message": "success", "email": result["email"]})


@app.route("/article", methods=["POST"])
@authorize
def post_article(user):
    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5002, debug=True)
