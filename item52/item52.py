import sqlite3


conn = sqlite3.connect('item38')
c = conn.cursor()

def tableCreate():
    c.execute("CREATE TABLE stuffToPlot (ID INT, unix REAL, datestamp TEXT, keyword TEXT, value REAL)")

def dataEntry():
    c.execute("INSERT INTO stuffToPlot VALUE
