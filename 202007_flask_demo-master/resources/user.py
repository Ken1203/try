from flask import jsonify, make_response
from flask_restful import Resource, reqparse
import pymysql


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class Users(Resource):

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
    sql = 'SELECT * FROM flask_demo.users Where deleted = False;'
    cursor.execute(sql)
    users = cursor.fetchall()
    db.close()
    return jsonify(users)

  def post(self):
    db, cursor = self.db_init()
    arg = parser.parse_args()
    user = {
      'name': arg['name'],
      'gender': arg['gender'],
      'birth': arg['birth'] or '1900-01-01',
      'note': arg['note']
    }

    sql = """
      INSERT INTO `flask_demo`.`users` (`name`, `gender`, `birth`, `note`) 
      VALUES ('{}', '{}', '{}', '{}');
    """.format(user['name'], user['gender'], user['birth'], user['note'])
    result = cursor.execute(sql)
    db.commit()
    db.close()
    response = {"msg": "success"}
    code = 201
    if result == 0:
      response['msg'] = 'error'
      code = 400
    return make_response(jsonify(response), code)


class User(Resource):
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
    sql = 'SELECT * FROM flask_demo.users Where id = {}'.format(id)
    cursor.execute(sql)
    user = cursor.fetchone()
    db.close()
    return jsonify(user)

  def patch(self, id):
    db, cursor = self.db_init()
    arg = parser.parse_args()
    user = {
      'name': arg['name'],
      'gender': arg['gender'],
      'birth': arg['birth'] or '1900-01-01',
      'note': arg['note']
    }

    query = []
    for key, value in user.items():
      if value != None:
        query.append(key + " = " + " '{}' ".format(value))
    query = ",".join(query)

    sql = """
    UPDATE `flask_demo`.`users` 
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
    UPDATE `flask_demo`.`users` 
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