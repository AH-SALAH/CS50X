"""
Author: AH-SALAH
DBQ.py (c) 2021
Desc: add DBQ.py
Created: 2021-05-22T20:42:57.120Z
Modified: 2021-05-23T14:56:15.719Z
"""

import sqlite3


class DBQ:
    def __init__(self):
        self.conn = {}
        self.cr = {}

    def dbConnect(self, dbPath):
        try:
            with sqlite3.connect(dbPath) as self.conn:
                # self.conn = sqlite3.connect(dbPath)
                if self.conn:
                    self.cr = self.conn.cursor()
                    print("DB connected successfully..")
        except sqlite3.Error as er:
            print("DB connection err: ", er)

    def getSchema(self, table=""):
        if table:
            # self.cr.execute("PRAGMA table_info('?')", [table])
            self.cr.execute(f"SELECT * FROM {table}")
        else:
            self.cr.execute("select name from sqlite_master where type = 'table';")
        print(self.cr.fetchall())

    #1 query to list the names of all songs in the database
    def getAllCol(self, col, table):
        resp = self.cr.execute(f"SELECT {col} FROM {table}")
        self.conn.commit()
        return resp

    #2 query to list the names of all songs in increasing order of tempo
    def getAllOrderdByCol(self, col, table, orderBy, orderType=""):
        resp = self.cr.execute(
            f"SELECT {col} FROM {table} ORDER BY {orderBy} {orderType}"
        )
        self.conn.commit()
        return resp

    #3 query to list the names of the top 5 longest songs, in descending order of length
    def getTopCountOrderdByCol(self, col, table, orderBy, orderType="", limit=5):
        resp = self.cr.execute(
            f"SELECT {col} FROM {table} ORDER BY {orderBy} {orderType} LIMIT {limit}"
        )
        self.conn.commit()
        return resp

    #4 query that lists the names of any songs that have danceability, energy, and valence greater than 0.75
    def getGreaterThan(self, col, table, value=0):
        resp = self.cr.execute(
            f"SELECT {col} FROM {table} WHERE danceability > ? AND energy > ? AND valence > ?",
            [value, value, value],
        )
        self.conn.commit()
        return resp

    #5 query that returns the average energy of all the songs
    def getAvg(self, col, table):
        resp = self.cr.execute(f"SELECT AVG({col}) FROM {table}")
        self.conn.commit()
        return resp

    #6 query that lists the names of songs that are by Post Malone
    def getPostMaloneSongs(self):
        resp = self.cr.execute(
            f"""
        SELECT songs.name FROM songs 
        JOIN artists 
        ON songs.artist_id = artists.id 
        WHERE artists.name = 'Post Malone'
        """
        )
        self.conn.commit()
        return resp

    #7 query that returns the average energy of songs that are by Drake
    def getDrakeSongsEnergy(self):
        resp = self.cr.execute(
            f"""
        SELECT AVG(songs.energy) FROM songs 
        JOIN artists 
        ON songs.artist_id = artists.id 
        WHERE artists.name = 'Drake'
        """
        )
        self.conn.commit()
        return resp

    #8 query that lists the names of the songs that feature other artists
    def getFeatSongs(self, col, table):
        resp = self.cr.execute(f"""SELECT {col} FROM {table} WHERE ? LIKE '%?%'""", ('name', 'feat'))
        self.conn.commit()
        return resp

    # def closeConn(self):
    #     self.cr.close()
    #     print("DB Closed Succesfully")
