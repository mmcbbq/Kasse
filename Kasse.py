import mysql.connector
import datetime


def find_produkt():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="Supermarkt")

	cursor = mydb.cursor()
	cursor.execute("SELECT * FROM produkte where Barcode = '123456';")
	result = cursor.fetchall()
	return result


def neuen_kassenzettel():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="Supermarkt")

	cursor = mydb.cursor()
	sql = "INSERT INTO kassenzettel ( Datum) VALUES (%s)"
	val = (datetime.datetime.now(),)
	cursor.execute(sql, val)
	mydb.commit()
	return cursor.lastrowid


def produkt_zu_kassenzettel(barcode, kassenzettel_id, menge):
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="Supermarkt")
	cursor = mydb.cursor()
	sql = "INSERT INTO produkte_kassenzettel (Barcode,Kassenzettel_ID, Menge) VALUES (%s, %s ,%s)"
	val = (barcode, kassenzettel_id, menge)
	cursor.execute(sql, val)
	mydb.commit()
	return cursor.lastrowid


def check_barcode(barcode):
	if   10000000 <= barcode <= 99999999:
		return True
	else:
		return False




