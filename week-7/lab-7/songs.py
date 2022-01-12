"""
Author: AH-SALAH
songs.py (c) 2021
Desc: add songs.py
Created: 2021-05-22T20:29:05.125Z
Modified: 2021-05-24T20:08:07.866Z
"""

from DBQ import DBQ


def main():
    db = DBQ()
    db.dbConnect("db/songs.db")
    # db.getSchema()

    # all = db.getAllCol('name', 'songs')
    # for r in all:
    #     print(r)

    # tempoOrdered = db.getAllOrderdByCol('name', 'songs', 'tempo')
    # for r in tempoOrdered:
    #     print(r)

    # top5 = db.getTopCountOrderdByCol('name', 'songs', 'duration_ms', 'DESC')
    # for r in top5:
    #     print(r)

    # greaterThan = db.getAvg('energy', 'songs')
    # for r in greaterThan:
    #     print(r)

    # postMalon = db.getPostMaloneSongs()
    # for r in postMalon:
    #     print(r)

    # drakeEnergy = db.getDrakeSongsEnergy()
    # for r in drakeEnergy:
    #     print(r)
    
    # drakeEnergy = db.getFeatSongs('name', 'songs')
    # for r in drakeEnergy:
    #     print(r)

    # db.closeConn()


if __name__ == "__main__":
    main()
