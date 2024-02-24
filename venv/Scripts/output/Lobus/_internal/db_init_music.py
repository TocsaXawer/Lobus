import mysql.connector
import asyncio
import datetime
import uuid

class db_music():
    def __init__(self, db):
        self.host = db[0]
        self.user = db[1]
        self.passwd = db[2]
        self.db = db[3]

    def connect(self):
        connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.db
            ) 
        return connection

    def get_music(self):
        try:
            connect = self.connect()
            cursor = connect.cursor()
            cursor.execute("SELECT ID, Nev, Eloado FROM zenek")
            data = cursor.fetchall()
            direct = []
            for i in range(len(data)):
                direct.append({'id':data[i][0], 'name': data[i][1], 'auth': data[i][2]})
            return(direct)
        except mysql.connector.Error as error:
            print("Hiba történt az adatbáziskapcsolatban:", error)
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    def set_music(self, music_data):
        try:
            connect = self.connect()
            cursor = connect.cursor()
            sql = "INSERT INTO zenek (ID, Nev, Eloado, Zene, BoritoKepe) VALUES (%s, %s, %s, %s, %s)"
            val = (music_data[0], music_data[1], music_data[2], music_data[3], music_data[4])
            cursor.execute(sql, val)
            connect.commit()
        
        except mysql.connector.Error as error:
            print("Hiba történt az adatbáziskapcsolatban:", error)
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    def remove_by_ID(self, ID):
        try:
            connect = self.connect()
            cursor = connect.cursor()

            sql = "DELETE FROM zenek WHERE ID=%s"
            val = (ID,)

            cursor.execute(sql, val)
            connect.commit()

        except mysql.connector.Error as error:
            print("Hiba történt az adatbáziskapcsolatban:", error)
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    def show_thumbnail(self, id):
        try: 
            connect = self.connect()
            cusrsor = connect.cursor()

            sql = "SELECT BoritoKepe FROM zenek WHERE ID = %s"
            try:
                cusrsor.execute(sql, (id,))
                image_blob = cusrsor.fetchall()[0]
                return image_blob
            except:
                cusrsor.close()
                connect.close()
        except mysql.connector.Error as error:
            print("Hiba történt az adatbáziskapcsolatban:", error)
        finally:
            if cusrsor:
                cusrsor.close()
            if connect:
                connect.close()
    
    def get_music_descript(self, id):
        try:
            connect = self.connect()
            cursor = connect.cursor()

            sql = "SELECT Nev, Eloado FROM zenek WHERE ID = %s"

            try:
                cursor.execute(sql, (id,))
                song_blob = cursor.fetchall()[0]
                return song_blob
            except:
                cursor.close()
                connect.close()
        except mysql.connector.Error as error:
            print("Hibba történt a zene_lekérésnél", error)
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    def get_music_data(self, id):
        try:
            connect = self.connect()
            cursor = connect.cursor()

            sql = "SELECT Zene FROM zenek WHERE ID = %s"
            try:
                cursor.execute(sql, (id,))
                song_blob = cursor.fetchall()[0]
                return song_blob
            except:
                cursor.close()
                connect.close()
        except mysql.connector.Error as error:
            print("Hibba történt a zene_lekérésnél", error)
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()

    async def search_database(self, query):
        try:
            connect = await asyncio.to_thread(
                mysql.connector.connect,
                host=self.host,
                user=self.user,
                password=self.passwd,
                database=self.db
            )
            cursor = connect.cursor()

            # SQL lekérdezés összeállítása és végrehajtása
            search_query = "SELECT ID, NEV, Eloado FROM zenek WHERE Nev LIKE %s or Eloado Like %s"
            cursor.execute(search_query, ('%' + query + '%','%' + query + '%'))

            # Eredmények lekérése
            results = cursor.fetchall()

            return results
        except  Exception as e:
            print("Hiba történt a keresés során:", e)
            return []

        finally:
            if connect:
                cursor.close()
                connect.close()
    
    def create_playlist(self, nev, leiras, borito_kepe, tulajdonos_id):
        connect = self.connect()
        cursor = connect.cursor()
        try:
            id = str(uuid.uuid4())
            insert_playlist_query = "INSERT INTO Playlists (ID, Nev, Leiras, BoritoKepe, LetrehozasDatuma, TulajdonosAzonosito) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_playlist_query, (id, nev, leiras, borito_kepe, datetime.datetime.now() ,tulajdonos_id))
            connect.commit()

        except Exception as e:
            print(f"Hiba történt pl felvétel: {e}")
            connect.rollback()

    def get_playlist_name(self, own):
        connect = self.connect()
        cursor = connect.cursor()

        try:
            get_playlist_query = "SELECT ID, Nev, Leiras, LetrehozasDatuma  FROM Playlists WHERE TulajdonosAzonosito = %s"
            cursor.execute(get_playlist_query, (own,))
            playlist_data = cursor.fetchall()
            adat = []
            for i in range(len(playlist_data)):
                x = {
                    'ID': playlist_data[i][0],
                    'Name': playlist_data[i][1],
                    'Descript': playlist_data[i][2],
                    'Date': playlist_data[i][3]
                }
                adat.append(x)
            return adat
        except Exception as e:
            return(adat)
        
    def get_numbers_in_playlist(self, playlist_id):
        connect = self.connect()
        cursor = connect.cursor()
        try: 
            cursor.execute(f"SELECT ZeneID FROM ZenePlaylistKapcsolo WHERE PlaylistID = '{playlist_id}'")
            zene_ids = [row[0] for row in cursor.fetchall()]
            return zene_ids
        except Exception as e:
            return (f"Hiba {e}")
        finally:
            if connect:
                cursor.close()
                connect.close()
                

    def remove_song_in_playlist(self, PID, SID):
        try:
            connect = self.connect()
            cursor = connect.cursor()
        
            sql = "DELETE FROM ZenePlaylistKapcsolo WHERE PlaylistID = %s AND ZeneID = %s"
            cursor.execute(sql, (PID, SID,))
            connect.commit()
        except:
            return 'hiba'
        finally:
            if connect:
                connect.close()
        

       
    def remove_playlist(self, id):
        try:
            connect = self.connect()
            cursor = connect.cursor()

            sql = "DELETE FROM Playlists WHERE ID=%s"
            val = (id,)

            cursor.execute(sql, val)
            connect.commit()
        except:
            return 'Hiba'
    
    def add_song_to_playlist(self, playlist_id, music_id):
        connect = self.connect()
        cursor = connect.cursor()

        try:
            # Ellenőrzés, hogy a lejátszási lista és a zene létezik-e az adatbázisban
            cursor.execute("SELECT * FROM Playlists WHERE ID = %s", (playlist_id,))
            playlist = cursor.fetchone()
            cursor.execute("SELECT * FROM Zenek WHERE ID = %s", (music_id,))
            music = cursor.fetchone()

            if not playlist or not music:
                return "A lejátszási lista vagy a zene nem található az adatbázisban."
            
            cursor.execute("INSERT INTO zeneplaylistKapcsolo (PlaylistID, ZeneID) VALUES (%s, %s)", (playlist_id, music_id))
            connect.commit()
        except mysql.connector.Error as err: 
            return f"Hiba az adatbáziskapcsolat során: {err}"
        finally:
            if connect:
                connect.close()

def watcher(datas):
    watch = datas.get_music()
    print(watch)

db = ['localhost', 'root', 'Adm1n', 'mydatabase']
datas = db_music(db=db)

