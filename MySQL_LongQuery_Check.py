#!/usr/bin/python
######
## Author: Luke Shirnia
# Github: https://github.com/LukeShirnia/MySQLProcessCheck

import subprocess
import MySQLdb
import time
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart


def send_email_test(long_query):
	'''
	Send an email once a long query has been acknowledged
	'''
	msg = MIMEMultipart()
	msg['To'] = email.utils.formataddr(('Recipient', 'to@address.com'))
	msg['From'] = email.utils.formataddr(('LukesLinuxPython', 'from@address.com'))
	msg['Subject'] = 'Long Running Query!'
	body_string = '\n'.join(long_query)
#	print body_string # Can be used to debug if mysql queries are being sent to email function correctly
	body = body_string
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('127.0.0.1') # Requires 127. and NOT localhost on some devices. It tries to connect to IPv6 locally and this may not be enabled in "mynetworks" in postfix
	text = msg.as_string()
#	server.set_debuglevel(True) # debug mail if required
	server.sendmail('from@address.com', ['to@address.com.com'], text)
	server.quit()
	subprocess.call(["/usr/bin/logger -s 'MySQLProcessCheck: Email Sent - '`date`"], shell=True) # add a log entry for the restart


def mysql_check(): 
	'''
	Connect to mysql and show the process list
	'''
	all_queries = []
	exclude_queries = ['Sleep', 'Binlog Dump'] # Exclude sleeping connected users and replication process

	query_string_headers = ["ID", "User", "Host", "DB", "State", "Query Time", "State", "Query"] 
	db = MySQLdb.connect(host="", user="", passwd="", db="")
	cur = db.cursor()
	cur.execute("show full processlist;")
	for row in cur.fetchall() :
		if int(row[5]) > 10 and row[4] not in exclude_queries:
	        	long_query = "ID: %s  User: %s Host: %s DB: %s State: %s  Query Time: %s State: %s Query: %s"  % ( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] )
#			print long_query # Used to see if queries are being picked up
			all_queries.append(long_query)
	all_queries = filter(None, all_queries)
	if len(all_queries) >= 1:
		send_email_test(all_queries)
	cur.close()
	db.close ()



try:
	mysql_check()
except Exception as error:
	print error
#	subprocess.call(["/usr/bin/logger -s error"], shell=True)
