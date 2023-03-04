from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import json
import pymysql
import hashlib
import datetime
import time
import secrets


def russian_number_validation(num: str):
    if not num.startswith("+7"):
        return False
    if len(num) != 12:
        return False
    for i in num[2:]:
        if not i.isdigit():
            return False
    return True


def format_russian_number(num: str):
    ik = "() -_"
    ext = num
    for i in ik:
        ext = ext.replace(i, '')
    return ext


def insert_token(user_id: int, time_inserted: datetime.datetime, time_to_be: int, cur):
    token_generated = secrets.token_hex(64)
    expires = datetime.datetime.utcfromtimestamp(time_inserted.timestamp()+time_to_be).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(sqls[3].format(token_generated, user_id, expires))
    return token_generated, expires


# configuration
app = Flask(__name__)
swagger_config = json.load(open('config.json'))
swagger = Swagger(app, swagger_config)

# DB
mf = '%Y-%m-%d %H:%M:%S'
con = pymysql.connect(
    host='demo_1_mysql',
    user='root', 
    password=open("secrets.txt").read(),
    database='main',
    cursorclass=pymysql.cursors.DictCursor
)

sqls = ["INSERT INTO user (`phone`, `password_hash`) VALUES(\"{}\", \"{}\")", "SELECT * FROM `user` WHERE phone=\"{}\";",
        "SELECT * FROM `user_token` WHERE user_id=\"{}\"", "INSERT INTO `user_token` (`token`, `user_id`, `expires`) VALUES(\"{}\", {}, \"{}\")" 
        ]


@app.route("/auth/v.1.0", methods=["POST"])
@swag_from("auth.yml", methods=["POST"])
def auth():
    if request.method == "POST":
        cur = con.cursor()
        req_data = request.get_json()
        phone = format_russian_number(req_data.get('phone'))
        password_hash = hashlib.md5(req_data.get('password').encode()).hexdigest()
        sql = sqls[1].format(phone)
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) > 0:
            x: datetime.datetime = result[0]['date_insert']
            if result[0]['password_hash'] == password_hash:
                cur.execute(sqls[2].format(result[0]["id"]))
                token_data = cur.fetchall()
                if len(token_data) > 0:
                    if token_data[0]["expires"].timestamp() > round(time.time()):
                        token = token_data[0]["token"]
                        expires = token_data[0]["expires"].strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        ret = {"success": False, "error": 'Токен просрочен', "data": {}, "message": 'token expired'}
                        return ret
                else:
                        token, expires = insert_token(result[0]["id"], result[0]['date_insert'], 18000, cur) 

                ret = {"success": True, "error": '', "data": {"token": token, "expires": expires}, "message": "successfull login"}
            else:
                ret = {"success": False, "error": "Неправильный пароль", "data": {}, "message": "incorrect password"}
        else:
            if russian_number_validation(phone):
                sql = sqls[0].format(phone, password_hash)
                cur.execute(sql)
                cur.execute(sqls[1].format(phone))
                result = cur.fetchall()
                token, expires = insert_token(result[0]["id"], result[0]['date_insert'], 18000, cur)
                ret = {"success": True, "error": '', "data": {"token": token, "expires": expires}, "message": "successfull registartion"}
            else:
                ret = {"success": False, "error": 'Номер телефона некорректен', "data": {}, "message": "invalid phone number"}
        con.commit()
        return jsonify(ret)


@app.route("/")
def index():
    return """
<a href='/api/'> Swagger </a>
    """