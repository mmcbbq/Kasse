import mysql.connector
import datetime


def find_produkt(barcode):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Supermarkt")

    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM produkte where Barcode = {barcode};")
    result = cursor.fetchall()
    return result[0]


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
    if 10000000 <= barcode <= 99999999:
        return True
    else:
        return False


def get_produkte(*barcode):
    produkte = []
    for x in barcode:
        produkte.append(find_produkt(x))
    return produkte


def get_preis(kassenzettel_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Supermarkt")

    cursor = mydb.cursor()

    cursor.execute(f"""SELECT pk.Kassenzettel_ID ,pk.Menge, P.Preis, P.Mwst
    FROM Produkte_Kassenzettel pk
    left join Produkte P on P.Barcode = pk.Barcode
    where pk.Kassenzettel_ID = {kassenzettel_id}""")

    result = cursor.fetchall()
    summe = 0
    for i in result:
        summe += round((i[2] + (i[2] * i[3] / 100)) * i[1], 2)
    return summe


def make_kassenzettel(einkaufsliste):
    kassen_id = neuen_kassenzettel()
    for pos in einkaufsliste:
        produkt_zu_kassenzettel(pos[0], kassen_id, pos[1])
    return kassen_id


def wechsel(bezahlt, preis):
    geld = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    if preis > bezahlt:
        return

    wechselgeld = round(bezahlt - preis, 2)
    # ->15.36 -> 10  5.36 -> 5 0.36 -> 0.2 -> 0.16 -> 0.10 ->0.6 > 0.05-> 0.01 0.01
    wg_liste = []

    while wechselgeld > 0:

        for geldschein in geld:
            if geldschein <= wechselgeld:
                wechselgeld = round(wechselgeld - geldschein, 2)
                wg_liste.append(geldschein)
                break
    return wg_liste


def print_kassenzettel(kassenzettel_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Supermarkt")

    cursor = mydb.cursor()

    cursor.execute(f"""SELECT pk.Kassenzettel_ID ,pk.Menge, P.Preis, P.Mwst, P.Name, P.Barcode
    FROM Produkte_Kassenzettel pk
    left join Produkte P on P.Barcode = pk.Barcode
    where pk.Kassenzettel_ID = {kassenzettel_id}""")
    result = cursor.fetchall()
    kassenzettel_string = f'Kassenzettel Nr.{kassenzettel_id}\n'
    stellen = 0
    for ele in result:
        preis_mit_mwst = round(ele[2] + (ele[2] * ele[3] / 100), 2)
        zeile = f'{ele[5]}{" " * (9 - len(str(ele[5])))}{ele[4]} {" " * (20 - len(ele[4]))} {preis_mit_mwst:.2f} Menge: {ele[1]} \t {round(preis_mit_mwst * ele[1], 2):.2f}€\n'
        kassenzettel_string += zeile
        if len(zeile) > stellen:
            stellen = len(zeile)
    summen_zeile = f"{' '*(stellen - 22)}gesamt Betrag {get_preis(kassenzettel_id)}€"
    kassenzettel_string += summen_zeile
    kassenzettel = open(f"Kassenzettel_{kassenzettel_id}.txt", "w")

    kassenzettel.write(kassenzettel_string)
    kassenzettel.close()


einkaufs_liste = [[2327921, 3], [3842669, 1], [4078005, 5], [41111635, 2], [44157548, 6]]

# kassenzettel_id = make_kassenzettel(einkaufs_liste)
# preis = get_preis(kassenzettel_id)
# bezahlt = int(input(f'Bitte {preis}'))
# print(wechsel(bezahlt, preis))
# print_kassenzettel(kassenzettel_id)
print_kassenzettel(5)
