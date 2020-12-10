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
    elif (userType == '2'):
        user(_conn)
    else:
        print("Please try again with a valid response")

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
        user(_conn)
    else:
        print("Please try again with a valid choice")

def user(_conn):
    print("""What would you like to search for?
    1: Players at a certain position
    2: Players under 6 feet
    3: Receivers that completed a pass
    4: Runners with at least any number of TDs
    5: Games with a final score difference less than one touchdown
    6: Search for a playerId
    7: Players that have both a rushing TD and no receiving fumbles
    8: Players that are 30 years old
    9: Linebackers with an interceptions and a number of sacks
    10: Players with the most solo tackles on their team
    11: Players with a pass defense and a sack
    12: Teams in the playoffs for a specific season
    13: Winners of superbowls
    14: Players that had a forced turnover
    15: Players with a rushing TD to the left and a catch
    16: Players that had a TD called back by a penalty
    17: Total rushing yeards in a game""")
    choice = int(input())

    if (choice == 1):
        allQBs(_conn)
    elif (choice == 2):
        under6(_conn)
    elif (choice == 3):
        receiverPass(_conn)
    elif (choice == 4):
        runner7(_conn)
    elif (choice == 5):
        gameScore(_conn)
    elif (choice == 6):
        playerId(_conn)
    elif (choice == 7):
        rushNoFum(_conn)
    elif (choice == 8):
        yo30(_conn)
    elif (choice == 9):
        pickSack(_conn)
    elif (choice == 10):
        mostSolo(_conn)
    elif (choice == 11):
        passSack(_conn)
    elif (choice == 12):
        playoffs(_conn)
    elif (choice == 13):
        superbowl(_conn)
    elif (choice == 14):
        forcedTurn(_conn)
    elif (choice == 15):
        rushLeft(_conn)
    elif (choice == 16):
        penalty(_conn)
    elif (choice == 17):
        totRushYds(_conn)
    else:
        print("Please try again with a valid entry")

def totRushYds(_conn):
    try:
        sql = """select G.gameId, sum(rushYards) as home
                from games as G, rusher as R, plays as P
                where G.gameId = P.gameId
                    and P.playId = R.playId
                    and G.homeTeamId = R.teamId
                UNION
                select G.gameId, sum(rushYards) as visitors
                from games as G, rusher as R, plays as P
                where G.gameId = P.gameId
                    and P.playId = R.playId
                    and G.visitorTeamId = R.teamId;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

def penalty(_conn):
    try:
        sql = """select playerId
                from rusher
                where rushPrimary = 1
                    and rushTd = 1
                    and rushNull = 1;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def rushLeft(_conn):
    try:
        sql = """select playerId
                from receiver
                where recNull = 0
                    and rec = 1
                    and recEnd = "in bounds"
                group by playerId
                INTERSECT
                select playerId
                from rusher
                where rushDirection = "left"
                    and rushPrimary = 1
                    and rushTd = 1
                    and rushNull = 0
                group by playerId;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def forcedTurn(_conn):
    try:
        sql = """select playerId
                from fumbles
                where fumType = "forced"
                    and fumTurnover = 1
                    and fumNull = 0
                group by playerId
                UNION
                select playerId
                from interceptions as I
                where I.intNull = 0
                    and I.int = 1
                group by playerId;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def superbowl(_conn):
    try:
        sql = """select season, winningTeam
                from games
                where seasonType = "SB";"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

def playoffs(_conn):
    try:
        _year = int(input("Enter in the year: "))
        sql = """select homeTeamId, visitorTeamId
                from games
                where seasonType != "PRE" 
                    and seasonType != "REG"
                    and season = ?;"""
        cursor = _conn.cursor()
        cursor.execute(sql, [_year])
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

def passSack(_conn):
    try:
        sql = """select P.nameFull, P.playerId
                from players as P, passDef as I, 
                        (SELECT playerId
                            from sacks
                            where sackNull = 0
                            group by playerId
                            having count(sackId) >= 1) as F
                where F.playerId = I.playerId
                    and I.passDefNull = 0
                    and F.playerId = P.playerId
                group by F.playerId
                having count(I.passDefId) >= 1;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

def mostSolo(_conn):
    try:
        sql = """select T1.playerId, sum(T1.tackleYdsScrim)
                from tackles as T1, tackles as T2
                where T1.teamId = T2.teamId
                    and T1.playerId != T2.playerId
                group by T1.teamId
                order by sum(T1.tackleYdsScrim) desc;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

def pickSack(_conn):
    try:
        _sack = int(input("Enter in the number of sacks you want to search for: "))
        sql = """select nameFull
                from interceptions as I, sacks as S, players as P
                where I.playerId = S.playerId
                    and P.playerId = I.playerId
                    and S.sackNull = 0
                    and sackPosition = "LB"
                    and I.intPosition = "LB"
                    and I.int = 1
                    and I.intNull = 0
                group by I.playerId
                having count(S.sackNull) = ?;"""
        cursor = _conn.cursor()
        cursor.execute(sql, [_sack])
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def yo30(_conn):
    try:
        sql = """select nameFull, dob
                from players
                where dob like "%1990";"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

def rushNoFum(_conn):
    try:
        sql = """select distinct nameFull
                from players as P, rusher as RB, receiver as RS
                where P.playerID = RB.playerID
                    and RB.playerID = RS.playerID
                    and RB.rushTD >= 1;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def playerId(_conn):
    try:
        _Id = int(input("Enter in the playerId you want to search for: "))
        sql = """select *
                from players
                where playerId = ?;"""
        cursor = _conn.cursor()
        cursor.execute(sql, [_Id])
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3]) + "|" + str(row[4]) + "|" + str(row[5]) + "\n"
        print(l)

    except Error as e:
        print(e)

def gameScore(_conn):
    try:
        sql = """select season, week, winningTeam
                from games
                where (homeTeamFinalScore - visitingTeamFinalScore) < 6;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)

def insert(_conn):
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

        try:
            sql = """insert into fumbles (fumId, playId, teamId, playerId, fumPosition, fumType, fumOOB, fumTurnover, fumNull) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            args = [_fumId, _playId, _teamId, _playerId, _fumPosition, _fumType, _fumOOB, _fumTurnover, _fumNull]
            _conn.execute(sql, args)
            print("Successfully inserted")
        except Error as e:
            print(e)

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

        try:
            sql = """insert into games(gameId, season, week, homeTeamId, visitorTeamId, seasonType, 
                weekNameAbbr, homeTeamFinalScore, visitingTeamFinalScore, winningTeam"""
            args = [_gameId, _season, _week, _homeTeamId, _visitorTeamId, _seasonType, _weekNameAbbr, _homeTeamFinalScore, _visitingTeamFinalScore, _winningTeam]
            _conn.execute(sql, args)
            print("Inserted successfully")
        except Error as e:
            print(e)

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

        try:
            sql = "insert into interceptions values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = [_interceptionId, _playId, _teamId, _playerId, _intPosition, _int, _intYards, _intTd, _intNull]
            _conn.execute(sql, args)
            print("Inserted into interceptions successfully")
        except Error as e:
            print(e)

    elif (choice == '4'):
        print("Inserting into passDef: ")
        _passDefId = int(input("Enter in the passDefId: "))
        _playId = int(input("Enter in the playId: "))
        _teamId = int(input("Enter in the teamId: "))
        _playerId = int(input("Enter in the playerId: "))
        _passDefPosition = input("Enter in the passDef Position: ")
        _passDefNull = int(input("Enter in the passDefNull: "))

        try:
            sql = "insert into passDef values(?, ?, ?, ?, ?, ?)"
            args = [_passDefId, _playId, _teamId, _playerId, _passDefPosition, _passDefNull]
            _conn.execute(sql, args)
        except Error as e:
            print(e)

    elif (choice == '5'):
        print("Inserting into passer: ")
        _passId = int(input("Enter in the passId: "))
        _playId = int(input("Enter in the playId: "))
        _teamId = int(input("Enter in the teamId: "))
        _playerId = int(input("Enter in the playerId: "))
        _passPosition = input("Enter in the passPosition: ")
        _passOutcome = input("Enter in the passOutcome: ")
        _passDirection = input("Enter in the passDirection: ")
        _passDepth = input("Enter in the passDepth: ")
        _passLength = int(input("Enter in the passLength: "))
        _passComp = int(input("Enter in the passComp: "))
        _passNull = int(input("Enter in the passNull: "))

        try:
            sql = "insert into passer values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = [_passId, _playId, _teamId, _playerId, _passPosition, _passOutcome, _passDirection, _passDepth, _passLength, _passComp, _passNull]
            _conn.execute(sql, args)
        except Error as e:
            print(e)

    elif (choice == '6'):
        print("Inserting into players: ")
        _playerId = int(input("Enter in the playerId: "))
        _nameFull = input("Enter in the nameFull: ")
        _position = input("Enter in the position: ")
        _heightInches = input("Enter in the heightInches: ")
        _weight = int(input("Enter in the weight: "))
        _dob = input("Enter in the dob: ")

        try:
            sql = "insert into player values(?, ?, ?, ?, ?, ?)"
            args = [_playerId, _nameFull, _position, _heightInches, _weight, _dob]
            _conn.execute(sql, args)
        except Error as e:
            print(e)

    elif (choice == '7'):
        print("Inserting into plays: ")
        _playId = int(input("Enter in the playId: "))
        _gameId = int(input("Enter in the gameId: "))
        _playSequence = int(input("Enter in the playSequence: "))
        _quarter = int(input("Enter in the quarter: "))
        _possessionTeam = int(input("Enter in the possessionTeam: "))
        _nonpossessionTeam = int(input("Enter in the nonpossessionTeam: "))
        _playType = input("Enter in the playType: ")
        _playType2 = input("Enter in the playType2: ")
        _playTypeDetailed = input("Eenter in the playTypeDetailed: ")
        _playNumberByTeam = int(input("Enter in the playNumberByTeam: "))
        _gameClock = int(input("Enter in the gameClockSecondsExpired: "))
        _gameClockStopped = int(input("Enter in the gameClockStoppedAfterPlay: "))
        _down = int(input("Enter in the down: "))
        _distance = int(input("Enter in the distance: "))
        _distanceToGoal = int(input("Enter in the distanceToGoalPre: "))
        _changePossession = int(input("Enter in the changePossession: "))
        _turnover = int(input("Enter in the turnover: "))
        _safety = int(input("Enter in the safety: "))
        _offYds = int(input("Enter in the offensiveYards: "))
        _netYards = int(input("Enter in the netYards: "))
        _firstDown = int(input("Enter in the firstDown: "))
        _effPlay = int(input("Enter in the efficientPlay: "))
        _scorePos = int(input("Enter in the scorePossession: "))
        _scoreNonPos = int(input("Enter in the scoreNonpossession: "))
        _homeScore = int(input("Enter in the homeScorePre: "))
        _visitingScore = int(input("Enter in the visitingScorePre: "))
        _homeScorePost = int(input("Enter in the homeScorePost: "))
        _visitingScorePost = int(input("Enter in the visitingScorePost: "))
        _distanceGoal = int(input("Enter in the distanceToGoalPost: "))

        try:
            sql = """insert into plays values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            args = [_playId, _gameId, _playSequence, _quarter, _possessionTeam, 
                _nonpossessionTeam, _playType, _playType2, _playTypeDetailed, 
                _playNumberByTeam, _gameClock, _gameClockStopped, _down, _distance,
                _distanceToGoal, _changePossession, _turnover, _safety, _offYds, _netYards, 
                _firstDown, _effPlay, _scorePos, _scoreNonPos, _homeScore, _visitingScore, 
                _homeScorePost, _visitingScorePost, _distanceGoal]
            _conn.execute(sql, args)
        
        except Error as e:
            print(e)

    elif (choice == '8'):
        print("Insert into receiver: ")
        _receiverId = int(input("Enter in the receiverId: "))
        _playId = int(input("Enter in the playId: "))
        _teamId = int(input("Enter in the teamId: "))
        _playerId = int(input("Enter in the playerId: "))
        _recPosition = input("Enter in the recPosition: ")
        _recYards = int(input("Enter in the recYards: "))
        _rec = int(input("Enter in the rec: "))
        _recYac = int(input("Enter in the recYac: "))
        _rec1down = int(input("Enter in the rec1down: "))
        _recEnd = input("Enter in the recEnd: ")
        _recNull = int(input("Enter in the recNull: "))

        try:
            sql = """insert into receiver values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            args = [_receiverId, _playId, _teamId, _playerId, _recPosition, _recYards, _rec, _recYac, _rec1down, _recEnd, _recNull]
            _conn.execute(sql, args)
            print("Inserted successfully")

        except Error as e:
            print(e)

    elif (choice == '9'):
        print("Insert into rusher: ")
        _rushId = int(input("Enter in the rushId: "))
        _playId = int(input("Enter in the playId: "))
        _teamId = int(input("Enter in the teamId: "))
        _playerId = int(input("Enter in the playerId: "))
        _rushPosition = input("Enter in the rushPosition: ")
        _rushType = input("Enter in the rushType: ")
        _rushDirection = input("Enter in the rushDirection: ")
        _rushLandmark = input("Enter in the rushLandmark: ")
        _rushYards = int(input("Enter in the rushYards: "))
        _rushPrimary = int(input("Enter in the rushPrimary: "))
        _rushTd = int(input("Enter in the rushTd: "))
        _rushEnd = input("Enter in the rushEnd: ")
        _rushNull = int(input("Enter in the rushNull: "))

        try:
            sql = """insert into rusher values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            args = [_rushId, _playId, _teamId, _playerId, _rushPosition, _rushType, _rushDirection, 
                _rushLandmark, _rushYards, _rushPrimary, _rushTd, _rushEnd, _rushNull]
            _conn.execute(sql, args)
            print("Inserted into rusher successfully")

        except Error as e:
            print(e)

    elif (choice == '10'):
        print("Insert into sacks: ")
        _sackId = int(input("Enter in the sackId: "))
        _playId = int(input("Enter in the playId: "))
        _teamId = int(input("Enter in the teamId: "))
        _playerId = int(input("Enter in the playerId: "))
        _sackPosition = input("Enter in the sackPosition: ")
        _sackYards = int(input("Enter in the sackYards: "))
        _sackNull = int(input("Enter in the sackNull: "))

        try:
            sql = """insert into rusher values(?, ?, ?, ?, ?, ?, ?)"""
            args = [_sackId, _playId, _teamId, _playerId, _sackPosition, 
                _sackYards, _sackNull]
            _conn.execute(sql, args)
            print("Inserted into sacks successfully")

        except Error as e:
            print(e)

    elif (choice == '11'):
        print("Insert into tackles: ")
        _tackleId = int(input("Enter in the tackleId: "))
        _playId = int(input("Enter in the playId: "))
        _teamId = int(input("Enter in the teamId: "))
        _playerId = int(input("Enter in the playerId: "))
        _tacklePosition = input("Enter in the tacklePosition: ")
        _tackleType = input("Enter in the tackleType: ")
        _tackleYdsScrim = int(input("Enter in the tackleYdsScrim: "))
        _tackleNull = int(input("Enter in the tackleNull: "))

        try:
            sql = """insert into tackles values(?, ?, ?, ?, ?, ?, ?, ?)"""
            args = [_tackleId, _playId, _teamId, _playerId, _tacklePosition, 
                _tackleType, _tackleYdsScrim, _tackleNull]
            _conn.execute(sql, args)
            print("Inserted into tackles successfully")

        except Error as e:
            print(e)

def update(_conn):
    out = """Which table would you like to update?
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

    if (choice == "1"):
        updateFumbles(_conn)
    elif (choice == '2'):
        updateGames(_conn)
    elif (choice == '3'):
        updateInterceptions(_conn)
    # elif (choice == '4'):
    #     updatePassDef(_conn)
    # elif (choice == '5'):
    #     updatePasser(_conn)
    elif (choice == '6'):
        updatePlayers(_conn)
    # elif (choice == '7'):
    #     updatePlays(_conn)
    # elif (choice == '8'):
    #     updateReceiver(_conn)
    # elif (choice == '9'):
    #     updateRusher(_conn)
    # elif (choice == '10'):
    #     updateSacks(_conn)
    # elif (choice == '11'):
    #     updateTackles(_conn)
    else:
        print("Please try again with a valid choice")

def delete(_conn):
    out = """Which table would you like to delete from?
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

    if (choice == "1"):
        deleteFumble(_conn)
    elif (choice == '2'):
        deleteGame(_conn)
    elif (choice == '3'):
        deleteInterception(_conn)
    # elif (choice == '4'):
    #     deletePassDef(_conn)
    # elif (choice == '5'):
    #     deletePasser(_conn)
    elif (choice == '6'):
        deletePlayer(_conn)
    # elif (choice == '7'):
    #     deletePlay(_conn)
    # elif (choice == '8'):
    #     deleteReceiver(_conn)
    # elif (choice == '9'):
    #     deleteRusher(_conn)
    # elif (choice == '10'):
    #     deleteSack(_conn)
    # elif (choice == '11'):
    #     deleteTackle(_conn)
    else:
        print("Please try again with a valid choice")

def updateFumbles(_conn):
    _fumId = int(input("Enter the fumble's ID you want to update: "))

    out = """What do you want to update? 
    1. Play ID
    2. Team ID
    3. Player ID
    4. Fumble Position
    5. Fumble Type
    6. Fumble OOB
    7. Fumble Turnover
    8. Fumble Null"""

    print(out)
    choice = input()

    if (choice == "1"):
        _playId = int(input("Enter in the new play ID: "))

        try:
            sql = """update fumbles 
                        set playId = ? 
                        where fumId = ?"""
            args = [_playId, _fumId]

            _conn.execute(sql, args)
            print("Updated play ID successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _teamId = int(input("Enter in the new team ID: "))

        try:
            sql = """update fumbles set teamId = ? where fumId = ?"""
            args = [_teamId, _fumId]

            _conn.execute(sql, args)
            print("Updated team ID successfully")

        except Error as e:
            print(e)

    elif (choice == '3'):
        _playerId = int(input("Enter in the new player ID: "))

        try:
            sql = """update fumbles set playerId = ? where fumId = ?"""
            args = [_playerId, _fumId]

            _conn.execute(sql, args)
            print("Updated player ID successfully")

        except Error as e:
            print(e)
    elif (choice == '4'):
        _fumPosition = input("Enter in the new fumble position: ")

        try:
            sql = """update fumbles set fumPosition = ? where fumId = ?"""
            args = [_fumPosition, _fumId]

            _conn.execute(sql, args)
            print("Updated fumble position successfully")

        except Error as e:
            print(e)
    elif (choice == '5'):
        _fumType = input("Enter in the new fumble type: ")

        try:
            sql = """update fumbles set fumType = ? where fumId = ?"""
            args = [_fumType, _fumId]

            _conn.execute(sql, args)
            print("Updated fumble type successfully")

        except Error as e:
            print(e)
    elif (choice == '6'):
        _fumOOB = int(input("Enter in the new fumble OOB: "))

        try:
            sql = """update fumbles set fumOOB = ? where fumId = ?"""
            args = [_fumOOB, _fumId]

            _conn.execute(sql, args)
            print("Updated fumble OOB successfully")

        except Error as e:
            print(e)
    elif (choice == '7'):
        _fumTurnover = int(input("Enter in the new fumble turnover: "))

        try:
            sql = """update fumbles set fumTurnover = ? where fumId = ?"""
            args = [_fumTurnover, _fumId]

            _conn.execute(sql, args)
            print("Updated fumble turnover successfully")

        except Error as e:
            print(e)
    elif (choice == '8'):   
        _fumNull = int(input("Enter in the new fumble null: "))

        try:
            sql = """update fumbles set fumNull = ? where fumId = ?"""
            args = [_fumNull, _fumId]

            _conn.execute(sql, args)
            print("Updated fumble null successfully")

        except Error as e:
            print(e)
    else:
        print("Please try again with a valid choice")

def updateGames(_conn):
    _gameId = int(input("Enter the game's ID you want to update: "))

    out = """What do you want to update? 
    1. Season
    2. Week
    3. Home Team ID
    4. Visitor Team ID
    5. Season Type
    6. Week Name Abbreviation
    7. Home Team Final Score
    8. Visiting Team Final Score
    9. Winning Team"""

    print(out)
    choice = input()

    if (choice == "1"):
        _season = int(input("Enter in the new season: "))
        try:
            sql = """update games 
                        set season = ? 
                        where gameId = ?"""
            args = [_season, _gameId]
            _conn.execute(sql, args)
            print("Updated season successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _week = int(input("Enter in the new week: "))
        try:
            sql = """update games set week = ? where gameId = ?"""
            args = [_week, _gameId]
            _conn.execute(sql, args)
            print("Updated season successfully")

        except Error as e:
            print(e)
    elif (choice == '3'):
        _homeTeamId = int(input("Enter in the new home team ID: "))

        try:
            sql = """update games set homeTeamId = ? where gameId = ?"""
            args = [_homeTeamId, _gameId]

            _conn.execute(sql, args)
            print("Updated home team ID successfully")

        except Error as e:
            print(e)
    elif (choice == '4'):
        _visitorTeamId = int(input("Enter in the new visiting team ID: "))

        try:
            sql = """update games set visitorTeamId = ? where gameId = ?"""
            args = [_visitorTeamId, _gameId]

            _conn.execute(sql, args)
            print("Updated players weight successfully")

        except Error as e:
            print(e)
    elif (choice == '5'):
        _seasonType = input("Enter in the new season type: ")

        try:
            sql = """update games set seasonType = ? where gameId = ?"""
            args = [_seasonType, _gameId]

            _conn.execute(sql, args)
            print("Updated season type successfully")

        except Error as e:
            print(e)

    elif(choice == '6'):
        _weekNameAbbr = input("Enter in the new week name abbreviation: ")

        try:
            sql = """update games set weekNameAbbr = ? where gameId = ?"""
            args = [_weekNameAbbr, _gameId]

            _conn.execute(sql, args)
            print("Updated week name abbreviation successfully")

        except Error as e:
            print(e)
    elif(choice == '7'):
        _homeTeamFinalScore = int(input("Enter in the new home team final score: "))

        try:
            sql = """update games set homeTeamFinalScore = ? where gameId = ?"""
            args = [_homeTeamFinalScore, _gameId]

            _conn.execute(sql, args)
            print("Updated home team final score successfully")

        except Error as e:
            print(e)
    elif(choice == '8'):
        _visitingTeamFinalScore = int(input("Enter in the new visiting team final score: "))

        try:
            sql = """update games set visitingTeamFinalScore = ? where gameId = ?"""
            args = [_visitingTeamFinalScore, _gameId]

            _conn.execute(sql, args)
            print("Updated visiting team final score successfully")

        except Error as e:
            print(e)
    elif(choice == '9'):
        _winningTeam = int(input("Enter in the new winning team: "))

        try:
            sql = """update players set winningTeam = ? where gameId = ?"""
            args = [_winningTeam, _gameId]

            _conn.execute(sql, args)
            print("Updated winning team successfully")

        except Error as e:
            print(e)
    else:
        print("Please try again with a valid choice")

def updateInterceptions(_conn):
    _interceptionId = int(input("Enter the interception's ID you want to update: "))

    out = """What do you want to update? 
    1. Play ID
    2. Team ID
    3. Player ID
    4. Interception Position
    5. Int
    6. Interception Yards
    7. Interception Touchdown
    8. Interception Null"""

    print(out)
    choice = input()

    if (choice == "1"):
        _playId = int(input("Enter in the new play ID: "))

        try:
            sql = """update interceptions 
                        set playId = ? 
                        where interceptionId = ?"""
            args = [_playId, _interceptionId]

            _conn.execute(sql, args)
            print("Updated play ID successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _teamId = int(input("Enter in the new team ID: "))

        try:
            sql = """update interceptions set teamId = ? where interceptionId = ?"""
            args = [_teamId, _interceptionId]

            _conn.execute(sql, args)
            print("Updated team ID successfully")

        except Error as e:
            print(e)

    elif (choice == '3'):
        _playerId = int(input("Enter in the new player ID: "))

        try:
            sql = """update interceptions set playerId = ? where interceptionId = ?"""
            args = [_playerId, _interceptionId]

            _conn.execute(sql, args)
            print("Updated player ID successfully")

        except Error as e:
            print(e)

    elif (choice == '4'):
        _intPosition = input("Enter in the new interception position: ")

        try:
            sql = """update interceptions set intPosition = ? where interceptionId = ?"""
            args = [_intPosition, _interceptionId]

            _conn.execute(sql, args)
            print("Updated interception position successfully")

        except Error as e:
            print(e)
    elif (choice == '5'):
        _int = int(input("Enter in the new int: "))

        try:
            sql = """update interceptions set int = ? where interceptionId = ?"""
            args = [_int, _interceptionId]

            _conn.execute(sql, args)
            print("Updated int successfully")

        except Error as e:
            print(e)
    elif (choice == '6'):
        _intYards = int(input("Enter in the new interception yards: "))

        try:
            sql = """update interceptions set intYards = ? where interceptionId = ?"""
            args = [_intYards, _interceptionId]

            _conn.execute(sql, args)
            print("Updated interception yards successfully")

        except Error as e:
            print(e)
    elif (choice == '7'):
        _intTd = int(input("Enter in the new interception touchdown: "))

        try:
            sql = """update interceptions set intTd = ? where interceptionId = ?"""
            args = [_intTd, _interceptionId]

            _conn.execute(sql, args)
            print("Updated interception touchdown successfully")

        except Error as e:
            print(e)
    elif (choice == '8'):
        _intNull = int(input("Enter in the new interception null: "))

        try:
            sql = """update interceptions set intNull = ? where interceptionId = ?"""
            args = [_intNull, _interceptionId]

            _conn.execute(sql, args)
            print("Updated interception null successfully")

        except Error as e:
            print(e)

def updatePlayers(_conn):
    _playerId = int(input("Enter the player's ID you want to update: "))
    
    out = """What do you want to update? 
    1. Name
    2. Position
    3. Height
    4. Weight
    5. Date of birth"""

    print(out)
    choice = input()

    if (choice == "1"):
        _nameFull = input("Enter in the new nameFull: ")

        try:
            sql = """update players 
                        set nameFull = ? 
                        where playerId = ?"""
            args = [_nameFull, _playerId]

            _conn.execute(sql, args)
            print("Updated players name successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _position = input("Enter in the new position: ")

        try:
            sql = """update players set position = ? where playerId = ?"""
            args = [_position, _playerId]

            _conn.execute(sql, args)
            print("Updated players position successfully")

        except Error as e:
            print(e)
    elif (choice == '3'):
        _heightInches = int(input("Enter in the new height: "))

        try:
            sql = """update players set heightInches = ? where playerId = ?"""
            args = [_heightInches, _playerId]

            _conn.execute(sql, args)
            print("Updated players height successfully")

        except Error as e:
            print(e)
    elif (choice == '4'):
        _weight = int(input("Enter in the new weight: "))

        try:
            sql = """update players set weight = ? where playerId = ?"""
            args = [_weight, _playerId]

            _conn.execute(sql, args)
            print("Updated players weight successfully")

        except Error as e:
            print(e)
    elif (choice == '5'):
        _dob = input("Enter in the new date of birth: ")

        try:
            sql = """update players set dob = ? where playerId = ?"""
            args = [_dob, _playerId]

            _conn.execute(sql, args)
            print("Updated players date of birth successfully")

        except Error as e:
            print(e)

    else:
        print("Please try again with a valid choice")

def deletePlayer(_conn):
    _playerId = input("Enter the playerId of the player you want to delete: ")

    try:
        sql = """delete from players where playerId = ?"""
        _conn.execute(sql, [_playerId])
        print("Deleted player successfully")

    except Error as e:
        print(e)

def allQBs(_conn):
    try:
        _name = input("Enter in the position you want to look for: ")
        sql = """select nameFull
                from players
                where position = ?;"""
        cursor = _conn.cursor()
        cursor.execute(sql, [_name])
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def under6(_conn):
    try:
        sql = """select nameFull
                from players
                where heightInches <= 72;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def receiverPass(_conn):
    try:
        sql = """select distinct nameFull
                from players as PL, passer as PR
                where PR.playerId = PL.playerId
                    and PR.passPosition = "WR"
                    and PR.passComp = 1;"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def runner7(_conn):
    try:
        _num = int(input("Enter in the number of TDs: "))
        sql = """select P.nameFull as Players
                from players as P, rusher as RS
                where P.playerID = RS.playerID
                    and P.position = "RB"
                group by P.playerID
                having count(RS.rushTd) >= ?;"""
        cursor = _conn.cursor()
        cursor.execute(sql, [_num])
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

def main():
    database = r"phase 2/NFLstats.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        setup(conn)

    closeConnection(conn, database)

if __name__ == '__main__':
    main()