import pyodbc

def selectByID(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE ID = ?"
    return cursor.execute(cmd, value)

def selectByName(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE NAMEOFBOOK = ?"
    return cursor.execute(cmd, value)

def selectByType(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE NAMEOFAUTHOR = ?"
    return cursor.execute(cmd, value)

def selectByAuthor(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE TYPEOFBOOK = ?"
    return cursor.execute(cmd, value)

def connect_to_SQL():
    return pyodbc.connect(
            "Driver={SQL Server};"
            "Server=tcp:LAPTOP-HV4IJC5O\SQLEXPRESS;"
            "PORT=1433;"
            "Database=LIBRARYDB;"
            "Trusted_Connection=yes;"
        )

cursor = selectByID("004")
for row in cursor:
    print("aaaa")
    print(row)

cursor = selectByName("Technical Writing For Dummies")
for row in cursor:
    print("aaaa")
    print(row)

cursor = selectByAuthor("Maggie Hamand")
for row in cursor:
    print("aaaa")
    print(row)

cursor = selectByType("STUDY")
for row in cursor:
    print("aaaa")
    print(row)
