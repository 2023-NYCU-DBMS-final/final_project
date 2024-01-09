import sqlite3

conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()
c.execute("select * from my_table where substr(SiteName,1,2)='板橋'")
print(c.fetchone())