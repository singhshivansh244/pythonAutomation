import sqlite3
import csv
from datetime import datetime 



conn = sqlite3.connect('Data.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    Link TEXT,
    Author TEXT,
    Headline TEXT,
    Date TEXT
)""")

csvLocation = str(datetime.today().strftime('%d%m%Y_verge.csv'))

with open(csvLocation, 'r') as file:
    csvreader = csv.reader(file)
    insertRecords = "INSERT INTO articles (Link, Author, Headline, Date) VALUES(?, ?, ?, ?)"
    cur.executemany(insertRecords, csvreader)

# cur.execute("""DROP TABLE articles""")


conn.commit()

conn.close()