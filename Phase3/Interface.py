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
    out = "Please enter 1 for admin or 2 for user: "
    print(out)
    userType = input()

    if (userType == '1'):
        admin(_conn)
    else:
        user(_conn)

def admin(_conn):
    out = """Please enter in a choice that you want to complete:
    1. Insert Information
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

def user(_conn):
    out = "Please choose a query that you would like to make: "

def insert(_conn):
    try:
        out = """Which table would you like to insert into?
        1. fumbles
        2. games
        3. interceptions
        4. passDef
        5. passer
        6. players
        7. plays
        8. receiver
        9. rusher
        10. sacks
        11. tackles"""

        print(out)
        choice = input()

        if (choice == '1'):
            print("Inserting into fumbles: ")
            _fumId = int(input("Enter in the fumId: "))
            _playId = int(input("Enter in the playId: "))
            _teamId = int(input("Enter in the teamId: "))
            _playerId = int(input("Enter in the playerId: "))
            _fumPosition = input("Enter in the fumPosition: ")
            _fumType = input("Enter in the fumType: ")
            _fumOOB = int(input("Enter in the fumOOB: "))
            _fumTurnover = int(input("Enter in the fumTurnover: "))
            _fumNull = int(input("Enter in the fumNull: "))

            sql = """insert into fumbles (fumId, playId, teamId, playerId, fumPosition, fumType, fumOOB, fumTurnover, fumNull) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            args = [_fumId, _playId, _teamId, _playerId, _fumPosition, _fumType, _fumOOB, _fumTurnover, _fumNull]
            _conn.execute(sql, args)
            print("Successfully inserted")

        elif(choice == '2'):
            print("Inserting into games: ")
            _gameId = int(input("Enter in the gameId: "))
            _season = int(input("Enter in the season: "))
            _week = int(input("Enter in the week: "))
            _homeTeamId = int(input("Enter in the homeTeamId: "))
            _visitorTeamId = int(input("Enter in the visitorTeamId: "))
            _seasonType = input("Enter in the seasonType: ")
            _weekNameAbbr = input("Enter in the weekNameAbbr: ")
            _homeTeamFinalScore = int(input("Enter in the homeTeamFinalScore: "))
            _visitingTeamFinalScore = int(input("Enter in the visitingTeamFinalScore: "))
            _winningTeam = int(input("Enter in the winningTeam: "))

            sql = """insert into games(gameId, season, week, homeTeamId, visitorTeamId, seasonType, 
                weekNameAbbr, homeTeamFinalScore, visitingTeamFinalScore, winningTeam"""
            args = [_gameId, _season, _week, _homeTeamId, _visitorTeamId, _seasonType, _weekNameAbbr, _homeTeamFinalScore, _visitingTeamFinalScore, _winningTeam]
            _conn.execute(sql, args)

        elif (choice == '3'):
            print("Inserting into interceptions: ")
            _interceptionId = int(input("Enter in the interceptionId: "))
            _playId = int(input("Enter in the playId: "))
            _teamId = int(input("Enter in the teamId: "))
            _playerId = int(input("Enter in the playerId: "))
            _intPosition = input("Enter in the intPosition: ")
            _int = int(input("Enter in the int: "))
            _intYards = int(input("Enter in the intYards: "))
            _intTd = int(input("Enter in the intTd: "))
            _intNull = int(input("Enter in the intNull: "))

            sql = "insert into interceptions values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = [_interceptionId, _playId, _teamId, _playerId, _intPosition, _int, _intYards, _intTd, _intNull]
            _conn.execute(sql, args)


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
