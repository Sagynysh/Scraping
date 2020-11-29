import psycopg2

hostname = 'localhost'
username = 'admin'
password = 'admin'
database = 'postgres'
def main():
	conn = psycopg2.connect(host=hostname,database=database,user=username,password=password,port='5432')

	cursor = conn.cursor()
	conn.autocommit = True
	sql = 'INSERT INTO bookStore (name, price, description, upc, stock, available, genre, rating) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
	val = ("test","test","test","test",False,4,"test",2)
	cursor.execute(sql,val)
	cursor.close()
	conn.close()


main()