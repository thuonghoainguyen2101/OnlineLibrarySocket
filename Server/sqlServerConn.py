import pyodbc

def selectByID(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE ID = ?"
    cursor.execute(cmd, value)
    return cursor

def selectByName(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE NAMEOFBOOK = ?"
    cursor.execute(cmd, value)
    return cursor

def selectByType(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE NAMEOFAUTHOR = ?"
    cursor.execute(cmd, value)
    return cursor

def selectByAuthor(value):
    conn = connect_to_SQL()
    cursor = conn.cursor()
    cmd = "SELECT * FROM BOOK WHERE TYPEOFBOOK = ?"
    cursor.execute(cmd, value)
    return cursor

def connect_to_SQL():
    return pyodbc.connect(
            "Driver={SQL Server};"
            "Server=tcp:LAPTOP-HV4IJC5O\SQLEXPRESS;"
            "PORT=1433;"
            "Database=LIBRARYDB;"
            "Trusted_Connection=yes;"
        )
