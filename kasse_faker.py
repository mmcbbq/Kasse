from faker import Faker
import faker_commerce
import mysql.connector
import random

fake = Faker()
fake.add_provider(faker_commerce.Provider)


def fake_preis():
    return round(random.uniform(0.01, 999.99), 2)


def fake_mwst():
    mwst = [19, 7]
    return mwst[random.randint(0, 1)]


def neuen_produkt():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Supermarkt")

    cursor = mydb.cursor()
    sql = "INSERT INTO produkte ( Barcode,Name, Preis, Mwst) VALUES (%s,%s,%s,%s)"
    val = (fake.ean(length=8), fake.ecommerce_name(), fake_preis(), fake_mwst())
    cursor.execute(sql, val)
    mydb.commit()
    return cursor.lastrowid


for i in range(1, 100):
    neuen_produkt()

# print(fake.ean(length=8))
# print(fake.ecommerce_name())
# print(fake_preis())
# print(fake_mwst())
