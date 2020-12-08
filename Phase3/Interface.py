import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print(" success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def setup(_conn):
    out = """Please enter in a choice that you want to complete:
    1. Insert Player
    2. Update Information
    3. Delete Information
    4. Search Stats"""

    print(out)
    choice = input()
    
    if (choice == '1'):
        insert(_conn)
    elif (choice == '2'):
        update(_conn)
    elif (choice == '3'):
        delete(_conn)
    elif (choice == '4'):
        search(_conn)
    else:
        print("Please try again with a valid choice")

def insert(_conn):
    try:
        sql = """insert into players()"""

    except Error as e:
        print(e)

def update(_conn):
    try:
        sql = ""

    except Error as e:
        print(e)

def delete(_conn):
    try:
        sql = ""

    except Error as e:
        print(e)

def search(_conn):
    try:
        sql = ""

    except Error as e:
        print(e)

def main():
    database = r"phase 2/NFLstats.sqlite"

    # create a database connection
    conn = openConnection(database)
    # with conn:
    #     dropTable(conn)
    #     createTable(conn)
    #     populateTable(conn)

    setup(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
