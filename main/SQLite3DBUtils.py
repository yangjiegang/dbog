import sqlite3
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )")
conn.commit()
# cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
# for row in cursor:
#     print "ID = ", row[0]
#     print "NAME = ", row[1]
#     print "ADDRESS = ", row[2]
#     print "SALARY = ", row[3], "\n"
my_timestamp = (1,)
c.execute('SELECT * FROM events WHERE ts = ?', my_timestamp)
conn.close()