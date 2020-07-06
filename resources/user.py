from flask import jsonify, make_response
from flask_restful import Resource,reqparse
import pymysql

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')



class Users(Resource):
	def db_init(self):
		db=pymysql.connect(
		'192.168.56.126',
		'ken',
		'3989889',
		'flack_demo'
		)
		cursor = db.cursor(pymysql.cursors.DictCursor)
		return db,cursor

	def get(self):
		db,cursor = self.db_init()
		sql ='SELECT * FROM flack_demo.users;'
		cursor.execute(sql)
		users = cursor.fetchall()
		db.close()
		return jsonify(users)
	def post(self):
		db,cursor = self.db_init()
		arg = parser.parse_args()#轉成dir
		user ={
			'name': arg['name'],
			'gender': arg['gender'],
			'birth': arg['birth'] or '1900-01-01',
			'note': arg['note']
		}

		sql = """
			INSERT INTO `flack_demo`.`users`(`name`,`gender`,`birth`,`note`)
			VALUES('{}','{}','{}','{}');
		""".format(user['name'],user['gender'],user['birth'],user['note'],)
		reslut = cursor.execute(sql)
		db.commit()
		db.close()

		response = {"msg":"success"}
		code = 201
		if reslut == 0:
			response['mag'] = 'error'
			code = 400
		
		return 	make_response(jsonify(response),code)



class User(Resource):
	def db_init(self):
		db=pymysql.connect(
		'192.168.56.126',
		'ken',
		'3989889',
		'flack_demo'
		)
		cursor = db.cursor(pymysql.cursors.DictCursor)
		return db,cursor




	def get(self,id):
		db,cursor = self.db_init()
		#sql ='SELECT * FROM flack_demo.users where id ={};'.format(id)
		sql ='SELECT * FROM flack_demo.users where deleted = False;'
		cursor.execute(sql)
		users = cursor.fetchall()
		db.close()
		return jsonify(users)

	def delete(self,id):
		db,cursor = self.db_init()
		sql ='UPDATE`flack_demo`.`users` SET deleted = True where id ={};'.format(id)
		#sql ='DELETE FROM `flack_demo`.`users` where id ={};'.format(id)
		reslut = cursor.execute(sql)
		db.commit()
		db.close()
		response = {"code ":200,"msg":"success"}
		if reslut == 0:
			response['mag'] = 'error'

		return 	jsonify(response)

	def patch(self,id):
		db,cursor = self.db_init()
		arg = parser.parse_args()#轉成dir
		user ={
			'name': arg['name'],
			'gender': arg['gender'],
			'birth': arg['birth'] or '1900-01-01',
			'note': arg['note']
		}

		query=[]
		for key, value in user.items():
			if value != None:
				query.append(key + "=" + "'{}'".format(value))
		query = ",".join(query)

		sql = """UPDATE `flack_demo`.`users` SET {} 'wewe' WHERE id = {};""".format(query, id)
		reslut = cursor.execute(sql)
		db.commit()
		db.close()
		response = {"code ":200,"msg":"success"}
		if reslut == 0:
			response['mag'] = 'error'

		return 	jsonify(response)

