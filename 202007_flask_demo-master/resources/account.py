from flask import jsonify
from flask_restful import Resource, reqparse
import pymysql

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('account_id')

class Accounts(Resource):

  def db_init(self):
    db = pymysql.connect(
      'localhost',
      'root',
      'password',
      'flask_demo'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

  def get(self):
    db, cursor = self.db_init()
    sql = 'SELECT * FROM flask_demo.accounts Where deleted = False;'
    cursor.execute(sql)
    accounts = cursor.fetchall()
    db.close()
    return jsonify(accounts)

  def post(self):
    db, cursor = self.db_init()
    arg = parser.parse_args()
    account = {
      'balance': arg['balance'] or 0,
      'account_number': arg['account_number'] or 12345,
      'account_id': arg['account_id'] or 0
    }

    sql = """
      INSERT INTO `flask_demo`.`accounts` (`balance`, `account_number`, `account_id`) 
      VALUES ('{}', '{}', '{}');
    """.format(account['balance'], account['account_number'], account['account_id'])
    result = cursor.execute(sql)
    db.commit()
    db.close()
    response = {"code": 200, "msg": "success"}
    if result == 0:
      response['msg'] = 'error'

    return jsonify(response)

class Account(Resource):
  def db_init(self):
    db = pymysql.connect(
      'localhost',
      'root',
      'password',
      'flask_demo'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor

  def get(self, id):
    db, cursor = self.db_init()
    sql = 'SELECT * FROM flask_demo.accounts Where id = {}'.format(id)
    cursor.execute(sql)
    account = cursor.fetchone()
    db.close()
    return jsonify(account)

  def patch(self, id):
    db, cursor = self.db_init()
    arg = parser.parse_args()
    account = {
      'balance': arg['balance'],
      'account_number': arg['account_number'],
      'account_id': arg['account_id']
    }

    query = []
    for key, value in account.items():
      if value != None:
        query.append(key + " = " + " '{}' ".format(value))
    query = ",".join(query)

    sql = """
    UPDATE `flask_demo`.`accounts` 
    SET {}
    WHERE id = {};
    """.format(query, id)

    result = cursor.execute(sql)
    db.commit()
    db.close()

    response = {"code": 200, "msg": "success"}
    if result == 0:
      response['msg'] = 'error'

    return jsonify(response)



  def delete(self, id):
    db, cursor = self.db_init()
    sql = """
    UPDATE `flask_demo`.`accounts` 
    SET deleted = True
    WHERE id = {};
    """.format(id)
    result = cursor.execute(sql)
    db.commit()
    db.close()

    response = {"code": 200, "msg": "success"}
    if result == 0:
      response['msg'] = 'error'

    return jsonify(response)