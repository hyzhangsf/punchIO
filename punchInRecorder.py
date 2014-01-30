#!/usr/bin/env python3

'''
Created on Jan 27, 2014

@author: zz
'''
import sys, sqlite3, os, time, datetime, getpass
# db = r'/Users/zz/example.db'
db = r'/usr/local/share/punch/example.db'
def printHelpMessage():
        print("** argument error.")
        print("** If you would like to punch in:")
        print("     $ punch in")
        print("** If you would like to punch out:")
        print("     $ punch out")   

def checkArgument():
    numberOfArguments = len(sys.argv)
    if numberOfArguments != 2:
        printHelpMessage()
        sys.exit(1)
    if sys.argv[1] in ["in","out","all","today","week"]:
        return sys.argv[1]
    else:
        printHelpMessage()

def checkIfDBFileExist(dbPath):
    return os.path.isfile(dbPath)

def createTable(conn, cur):
    cur.execute("CREATE TABLE activities(name text, punchInTime datetime, punchOutTime datetime, log text, duration time)")

def opendb(db):
    databaseExists = checkIfDBFileExist(db)
    if not  databaseExists:
        print ("CreatingDB.\n")
    conn = sqlite3.connect(db,10)
    cur = conn.cursor()
    if not  databaseExists:
        createTable(conn, cur)
    return [conn, cur]

def checkIsPunchedIn(db):
    conn, cur = opendb(db)
    r=cur.execute("select * from activities where PunchOutTime is null and name is ?",(getUserName(),)).fetchall()
    conn.close()
    if len(r) == 1:
        return True
    else:
        return False

def getUserName():
    return getpass.getuser()

def punchIn():
    if checkIsPunchedIn(db):
        print("you are already punched in")
        sys.exit(0)
    conn, cur = opendb(db)
    now = datetime.datetime.now()
    a=cur.execute("insert into activities (name, punchInTime, punchOutTime) values (?, ?, null);",(getUserName(),now,))
    conn.commit()
    conn.close()
    print("punched in at", now)

def punchOut():
    if checkIsPunchedIn(db):
        message = input("What did you do?\n -> ")
        conn, cur = opendb(db)
        now = datetime.datetime.now()
        cur.execute("update activities set punchOutTime=?  where punchOutTime is null and name is ?;", ( now, getUserName()))
        cur.execute("update activities set log=? where name is ? and punchOutTime is ?;", ( message, getUserName(),now ) )
        conn.commit()
        conn.close()
        print("pucnhed out at", now)
    else:
        print("you are not punched in")
def convertTimeStringToDatetime(timeString):
    #@param '2014-01-27 09:11:17.123'
    #@return datetime.datetime(2014, 1, 27, 9, 11, 17, 123000)
    return datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S.%f")

def all():
    if not checkIfDBFileExist(db):
        opendb(db)
        print("first time use, initializing database")
    assert(checkIfDBFileExist(db))
    conn, cur = opendb(db)    
    userName = getUserName()
    # records=cur.execute("select * from activities where name is ?  and punchOutTime is not null;", (userName,)).fetchall()
    records=cur.execute("select * from activities where punchOutTime is not null;").fetchall()

    for record in records:
        punchInTime, punchOutTime = convertTimeStringToDatetime(record[1]),convertTimeStringToDatetime(record[2])
        duration = punchOutTime - punchInTime
        seconds = duration.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = int(seconds % 60)

        print(record[0]," "*(15-len(record[0])),'|', punchInTime.strftime('%Y-%m-%d %H:%M:%S'),'|', punchOutTime.strftime('%Y-%m-%d %H:%M:%S'),'|','{} hours, {} minutes, {} seconds'.format(hours,minutes, seconds),'|',record[-2])


        
option = checkArgument()
if option ==  "in":
    punchIn()
if option == "out":
    punchOut()
if option == "all":
    # print daily summary
    all()
    # pass
if option == "week":
    # print weekly summary
    pass
