from flask import Flask
from flask import request
from flask_cors import CORS
import psycopg2
import json

app = Flask(__name__)
CORS(app)

hostname = 'localhost'
username = 'admin'
password = 'admin'
database = 'postgres'

conn = psycopg2.connect(host=hostname,database=database,user=username,password=password,port='5432')

@app.route("/search-books", methods=['GET'])
def search_books():
	cursor = conn.cursor()

	sql = 'select * from bookStore'
	params = ' WHERE '
	values = []

	if 'name' in request.args:
		name = request.args['name']
		params += 'name like %s and '
		values.append(name)

	if 'genre' in request.args:
		genre = request.args['genre']
		params += 'genre like %s and '
		values.append(genre)
	if 'rating' in request.args:
		rating = request.args['rating']
		params += 'rating = %s and '
		values.append(rating)

	if(len(params) != 7):
		params = params[0:len(params)-4]
		sql+=params

	print('Sql template')
	print(sql)

	book_list = []
	cursor.execute(sql,values)
	results = cursor.fetchall()
	for res in results:
		book = Book(res[1],res[2])
		book.detail_desc = res[3]
		book.upc = res[4]
		book.inStock = res[5]
		book.available = res[6]
		book.genre = res[7]
		book.rating = res[8]
		book_list.append(book)

	res = json.dumps([book.dump() for book in book_list],ensure_ascii=False, default=str)
	return res

class Book:
	genre = ''
	detail_desc = ''
	UPC = ''
	inStock = False
	available = 0
	rating = 0

	def __init__ (self, name, price):
		self.name = name
		self.price = price
	def dump(self):
		return {'name': self.name,'price': self.price,'desc': self.detail_desc,'upc': self.upc,'stock': self.inStock,'available': self.available,'genre': self.genre,'rating': self.rating}

if __name__ == "__main__":
    app.run()