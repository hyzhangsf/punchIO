#!/usr/bin/env python3

'''
Created on Jan 27, 2014

@author: zz
'''
import sys, sqlite3, os, time, datetime, getpass
db = r'/Users/zz/example.db'
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
    if sys.argv[1] in ["in","out","today","week"]:
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

def dailyReport():
    if not databaseExists(db):
        print("first time use, initializing database")
    conn, cur = opendb(db)
    assert(databaseExists(db))
    userName = getUserName()
        

option = checkArgument()
if option ==  "in":
    punchIn()
if option == "out":
    punchOut()
if option == "today":
    # print daily summary
    pass
if option == "week":
    # print weekly summary
    pass