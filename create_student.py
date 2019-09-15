import sqlite3
def add(Id,Name):
	conn = sqlite3.connect('student.db')
	
	conn.execute("insert into details(id,name)\
		values(%d,%s)" %(int(Id),Name))
	conn.commit()
	conn.close()
	return