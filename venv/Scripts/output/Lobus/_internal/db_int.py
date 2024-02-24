import mysql.connector
import hashlib

class db_int():
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.passwd = password
        self.db = db

    def checker(self, data_line):
        user = ""
        passwo = ""
        rang = ""
        data_line = list(data_line[0])
        data = self.get_user_by_id(data_line[0])
        data = list(data[0])
        if data_line[1]!="":
            if data_line[1] != data[1]: 
                user = data_line[1]
            else:
                user = data[1]
        else :
            user = data[1]
        if data_line[2] != "":
            if data_line[2] != data[2]:
                passwo = data_line[2]
            else:
                passwo = data[2]
        else:
            passwo = data[2]
        print(data_line[3], data[4])
        if data_line[3] != data[4]:
            rang = data_line[3]
        else:
            rang = data[4]

        self.update_user(id=data_line[0], username=user, passwd=passwo, rang=rang)
    
    def encrypt_string(self, password):
        sha_signature = \
            hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    def belepes(self, usr, pas):
        cursor = None
        connection = None
        try:
            
            # Adatbázis csatlakozás létrehozása
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.db
            )

            # Adatbázis cursor létrehozása
            cursor = connection.cursor()

            # Felhasználónevet és jelszót bekérjük
            felhasznalo_neve = usr
            jelszo = pas

            # SQL lekérdezés készítése és végrehajtása
            query = "SELECT nev, jelszo, rang, felhasznalo_id FROM Felhasznalok WHERE nev = %s"
            cursor.execute(query, (felhasznalo_neve,))

            # Lekérdezett adatok kiolvasása
            felhasznalo_adatok = cursor.fetchone()
            if felhasznalo_adatok:
                db_jelszo = felhasznalo_adatok[1]
                if self.encrypt_string(jelszo)== db_jelszo:
                    lista = list(felhasznalo_adatok)
                    return lista
                else:
                    return("HFP")
            else:
                return("NOF")

        except mysql.connector.Error as err:
            return("No db")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def get_user(self):
        try:
            # Adatbázis csatlakozás létrehozása
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.db
            )

            # Adatbázis cursor létrehozása
            cursor = connection.cursor()

            # SQL lekérdezés készítése és végrehajtása a kép feltöltéséhez
            cursor.execute("SELECT * FROM Felhasznalok")
            data = cursor.fetchall()
            return data
        except mysql.connector.Error as err:
            print("Hiba történt az adatbáziskapcsolatban:", err)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_user(self, id):
        try:
            # Adatbázis csatlakozás létrehozása
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.db
            )

            # MySQL kapcsolat létrehozása sikeres volt, így létrehozunk egy kurzort
            cursor = connection.cursor()

            # Rekord törlése az adatbázisból
            sql = "DELETE FROM Felhasznalok WHERE felhasznalo_id = %s"
            val = (id,)

            cursor.execute(sql, val)
            connection.commit()

        except mysql.connector.Error as err:
            print("Hiba történt az adatbáziskapcsolatban:", err)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
    def add_user(self, id, username, passwd, profil_kep, rang):
            try:
                # Adatbázis csatlakozás létrehozása
                connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.passwd,
                    database=self.db
                )

                # MySQL kapcsolat létrehozása sikeres volt, így létrehozunk egy kurzort
                cursor = connection.cursor()

                # Rekord törlése az adatbázisból
                sql = "INSERT INTO felhasznalok (felhasznalo_id, nev, jelszo, profil_kep, rang) VALUES (%s, %s, %s, %s, %s);"
                val = (id, username, passwd, profil_kep, rang)

                cursor.execute(sql, val)
                connection.commit()

            except mysql.connector.Error as err:
                print("Hiba történt az adatbáziskapcsolatban:", err)

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
    
    def get_user_by_id(self, id):
        try:
            connection = mysql.connector.connect(
                host = self.host, 
                user = self.user, 
                password = self.passwd,
                database = self.db
            )

            cursor = connection.cursor()

            sql = "SELECT * FROM felhasznalok WHERE felhasznalo_id = %s"

            cursor.execute(sql, (id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor :
                cursor.close()
            if connection:
                connection.close()
    
    def update_user(self, id, username, passwd, rang):
        try: 
            connection = mysql.connector.connect(
                host=self.host, 
                user = self.user, 
                password = self.passwd,
                database = self.db
            )

            cursor = connection.cursor()

            sql = "UPDATE felhasznalok SET nev = %s, jelszo = %s, rang = %s WHERE felhasznalo_id = %s;"

            cursor.execute(sql, (username, passwd, rang, id,))
            connection.commit()
        except mysql.connector.Error as err:
            print("Hiba történt az adatbáziskapcsolatban:", err)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def update_profil_pic(self, pic, id):
        # Adatbázis csatlakozás létrehozása
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            database=self.db
        )

        # MySQL kapcsolat létrehozása sikeres volt, így létrehozunk egy kurzort
        cursor = connection.cursor()

        # Képfájl beolvasása bináris módban

        # SQL lekérdezés a kép beszúrására
        sql = "UPDATE felhasznalok SET profil_kep = %s WHERE felhasznalo_id = %s"
        cursor.execute(sql, (pic, id))
        connection.commit()
        print("Kép sikeresen feltöltve.")

        # Kapcsolat lezárása
        connection.close()

    def show_image(self, id):
    # Adatbázis csatlakozás létrehozása
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.passwd,
            database=self.db
        )

        cursor = connection.cursor()

        # SQL lekérdezés a blob letöltésére az adatbázisból
        sql = "SELECT profil_kep FROM felhasznalok WHERE felhasznalo_id = %s"
        try:
            cursor.execute(sql, (id,))
            image_blob = cursor.fetchone()[0]
            return image_blob
        except:
            # Kapcsolat lezárása
            cursor.close()
            connection.close()

# Használat példája:
server = db_int(host='localhost', user='root', password='Adm1n', db='mydatabase')
#print(server.get_user_by_id(id=3))
#server.update_user(id=3, username="Mathe", passwd="Anyad", rang="Admin")