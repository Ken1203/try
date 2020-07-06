from flask import jsonify
from flask_restful import Resource, reqparse
import pymysql
parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')
# parser.add_argument('note')
class Accounts(Resource):
	def msg(self, result):
		response = {'code':200, "msg":'success'}
		if result==0:
			response['msg']='error'
		return jsonify(response)
	def db_init(self):
		db = pymysql.connect(
			'192.168.56.126',
		 'ken',
		 '3989889',
		 'flack_demo'
			)
		cursor = db.cursor(pymysql.cursors.DictCursor)
		return db,cursor
	def get(self):
		db, cursor = self.db_init()
		sql = 'SELECT * FROM flack_demo.account where deleted = False;'
		cursor.execute(sql)
		users = cursor.fetchall()
		db.close()
		return jsonify(users)
	def post(self):
		db, cursor = self.db_init()
		arg= parser.parse_args()
		account = {
			'balance':arg['balance'],
			'account_number':arg['account_number'] or 12345,
			'user_id':arg['user_id'] or 1,
			# 'note':arg['note'],
		}
		sql = """
			INSERT INTO `flack_demo`.`account` (`balance`, `account_number`, `user_id`)
			VALUES ('{}', '{}', '{}');
		""".format(account['balance'],account['account_number'],account['user_id'])
		result = cursor.execute(sql)
		db.commit()
		db.close()
		
		return self.msg(result)
class Account(Resource):
	def msg(self, result):
		response = {'code':200, "msg":'success'}
		if result==0:
			response['msg']='error'
		return jsonify(response)
	def db_init(self):
		db = pymysql.connect(
			'192.168.56.126',
		 'ken',
		 '3989889',
		 'flack_demo'
			)
		cursor = db.cursor(pymysql.cursors.DictCursor)
		return db,cursor
	def get(self, id):
		db, cursor = self.db_init()
		sql = 'SELECT * FROM flack_demo.account where id ={};'.format(id)
		cursor.execute(sql)
		user = cursor.fetchone()
		db.close()
		return jsonify(user)
	def delete(self, id):
		db, cursor = self.db_init()
		# sql = 'DELETE FROM `flask_demo`.`new_table` where id ={};'.format(id)
		sql = 'UPDATE `flack_demo`.`account` SET deleted = True where id ={};'.format(id)
		result = cursor.execute(sql)
		db.commit()
		db.close()
		return self.msg(result)
	def patch(self,id):
		db, cursor = self.db_init()
		arg= parser.parse_args()
		account = {
			'balance':arg['balance'],
			'account_number':arg['account_number'],
			'user_id':arg['user_id'],
		}
		query = []
		for key,value in account.items():
			if value != None:
				query.append(key + "=" + " '{}' ".format(value))
		query = ",".join(query)
		sql = """
		UPDATE `flack_demo`.`account`
		SET {} WHERE id = {};
		""".format(query,id)
		result = cursor.execute(sql)
		db.commit()
		db.close()
		return self.msg(result)


