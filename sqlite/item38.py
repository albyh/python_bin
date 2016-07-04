from __future__ import unicode_literals
import sqlite3

def printTable(c,all=True):
    if all:
        for row in c.fetchall():
            print(row)
    else:
        #while True:
        row = c.fetchone()
        #if row is None:
            #break
        print(row)        
#-------------------------------------------------
#1. Create a database table in RAM named Roster that includes the fields ‘Name’, ‘Species’ and ‘IQ’
roster = (
    ('Jean-Baptiste Zorg', 'Human', 122),
    ('Korben Dallas','Meat Popsicle', 100),
    ('Ak\'not','Mangalore', -5)
    )

#setup database and create cursor object
with sqlite3.connect(':memory:') as connection:
    #suppress 'u'on string output
    #connection.text_factory = str
    c=connection.cursor()
    c.execute("DROP TABLE IF EXISTS People")
    c.execute("CREATE TABLE Roster(Name TEXT, Species TEXT, IQ INT)")
    c.executemany("INSERT INTO Roster VALUES(?,?,?)",roster)

    c.execute("SELECT * from Roster")
    printTable(c)

#3. Update the Species of Korben Dallas to be Human
    print("***** Update KD Species *****")
    c.execute("UPDATE Roster SET Species = 'Human' WHERE Name = 'Korben Dallas'")
    c.execute("SELECT * from Roster")
    printTable(c)

#4. Display the names and IQs of everyone in the table who is classified as Human
    print("***** Print Humans *****")
    c.execute("SELECT Name,IQ FROM Roster WHERE species = 'Human'")
    printTable(c)
