import flask
from flask import request, jsonify
from flask_restful import Api, Resource
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql

app = flask.Flask(__name__)
app.config['DEBUG'] = True

api = Api(app)
api.add_resource(Users, "/users")
api.add_resource(User, "/user/<id>")
api.add_resource(Accounts, "/accounts")
api.add_resource(Account, "/account/<id>")

@app.errorhandler(Exception)
def handle(error):
  code = 500
  if type(error).__name__ == 'NotFound':
      code = 404
  return {
    'msg': type(error).__name__
  }, code


@app.before_request
def auth():
    token = request.headers.get('auth')
    if token == '567':
        pass
    else:
      return {
        'msg': 'invalid token',
      }, 401

@app.route('/', methods=['get'])
def home():
  return '<h2>so good</h2>'

@app.route('/account/<account_number>/deposit', methods=['post'])
def deposit(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balance'] + int(money)

    sql = """
        UPDATE `flask_demo`.`accounts` 
        SET `balance` = {}
        WHERE account_number = {};
    """.format(balance, account_number)
    result = cursor.execute(sql)
    db.commit()
    db.close()

    response = {"code": 200, "msg": "success"}
    if result == 0:
      response['msg'] = 'error'

    return jsonify(response)

@app.route('/account/<account_number>/withdraw', methods=['post'])
def withdraw(account_number):
  db, cursor, account = get_account(account_number)
  money = request.values['money']
  balance = account['balance'] - int(money)

  response = {"code": 200, "msg": "success"}
  if balance < 0:
    response['msg'] = 'error'
    response['code'] = 400
    return jsonify(response)
  else:
    sql = """
        UPDATE `flask_demo`.`accounts` 
        SET `balance` = {}
        WHERE account_number = {};
    """.format(balance, account_number)
    result = cursor.execute(sql)
    db.commit()
    db.close()
    return jsonify(response)
  
def get_account(account_number):
  db = pymysql.connect(
    'localhost',
    'root',
    'password',
    'flask_demo'
  )
  cursor = db.cursor(pymysql.cursors.DictCursor)
  sql = """
    SELECT * FROM flask_demo.accounts Where account_number = {}
  """.format(account_number)
  cursor.execute(sql)
  account = cursor.fetchone()

  return db, cursor, account



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3333)