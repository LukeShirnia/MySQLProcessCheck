
rt MySQLdb
import time
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart


def send_email_test(long_query): # Send an email once a long query has been acknowledged
	msg = MIMEMultipart()
	msg['To'] = email.utils.formataddr(('Recipient', 'luke@shirnia'))
	msg['From'] = email.utils.formataddr(('LukesLinuxPython', 'root@lukeslinux.co.uk'))
	msg['Subject'] = 'Long Running Query!'
	body_string = '\n'.join(long_query)
	print body_string
	body = body_string
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('localhost')
	text = msg.as_string()
	#server.set_debuglevel(True) # debug mail if required
	server.sendmail('root@lukeslinux', ['luke@shirnia.com'], text)
	server.quit()


def mysql_check(): # Connect to mysql and show the process list
	all_queries = []
	query_string_headers = ["ID", "User", "Host", "DB", "State", "Query Time", "State", "Query"] 
	db = MySQLdb.connect(host="", user="", passwd="", db="")
	cur = db.cursor()
	cur.execute("show full processlist;")
	for row in cur.fetchall() :
		if int(row[5]) > 10 and "Sleep" not in row[4]:
	        	long_query = "ID: %s  User: %s Host: %s DB: %s State: %s  Query Time: %s State: %s Query: %s"  % ( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] )
			print long_query
			all_queries.append(long_query)
	all_queries = filter(None, all_queries)
	if len(all_queries) > 1:
		send_email_test(all_queries)
	cur.close()
	db.close ()



try:
	mysql_check()
except Exception as error:
	print error
