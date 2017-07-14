import MySQLdb
import time

try:
	db = MySQLdb.connect(host="", user="", passwd="", db="")
	cur = db.cursor()

	cur.execute("show processlist;")
	for row in cur.fetchall() :
		if int(row[5]) > 10:
			#print row[5]
	        	print row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
 			#print row[5] #row 5 is the query time
	cur.close()
	db.close ()
except Exception as error:
	print error
