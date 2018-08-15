#!/usr/bin/env python
######
# Author: Luke Shirnia
# Github: https://github.com/LukeShirnia/MySQLProcessCheck

import __future__
import subprocess
import pymysql as db
import time
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# Change the settings below as required:
settings = {
    "Settings": {
        "QueryTime": 10  # In seconds
    },
    "MySQL": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "",
        "db": ""
    },
    "Email": {
        "Recipient": "",
        "From": "",
        "Subject": ""
    },
    "Logging": {
        "LogFile": "/home/mysql/longqueries"
    },
    "Queries": [  # Exclude the following queries
        "Sleep",
        "Binlog Dump"
    ]
}


def send_email_test(long_query):
    '''
    Send an email once a long query has been acknowledged
    '''
    msg = MIMEMultipart()
    msg['To'] = email.utils.formataddr(
        ('Recipient', settings["Email"]["Recipient"]))
    msg['From'] = email.utils.formataddr(
        ('LukesLinuxPython', settings["Email"]["From"]))
    msg['Subject'] = settings["Email"]["Subject"]
    body_string = '\n'.join(long_query)
    # print body_string # Can be used to debug if mysql queries are being sent
    # to email function correctly
    body = body_string
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('127.0.0.1')  # Requires 127. and NOT localhost on
    # some devices. It tries to connect to IPv6 locally and this may not be
    # enabled in "mynetworks" in postfix
    text = msg.as_string()
    # server.set_debuglevel(True) # debug mail if required
    server.sendmail(settings["Email"]["From"],
                    [settings["Email"]["Recipient"]], text)
    server.quit()
    subprocess.call(
        ["/usr/bin/logger -s 'MySQLProcessCheck: Email Sent - '`date`"],
        shell=True)  # add a log entry for the restart


def record_to_file(all_queries):
    '''
    Record all long running queries to a file with time stamp
    '''
    time_now = datetime.datetime.now()
    time_now_time = time_now.strftime('%b %d %H:%M')
    time_now_time = time_now_time + "\n"
    body_string = '\n'.join(all_queries)
    body_string = body_string + "\n" + "\n"
    with open(settings["Logging"]["LogFile"], "a") as file_:
        file_.write(time_now_time)
        file_.write(body_string)


class mysql_check():
    '''
    Connect to mysql and check the process list
    '''
    def __init__(self):
        self.all_queries = []

        self.exclude_queries = settings["Queries"]
        self.HOST = settings["MySQL"]["host"]
        self.PORT = settings["MySQL"]["port"]
        self.USER = settings["MySQL"]["user"]
        self.PASSWORD = settings["MySQL"]["password"]
        self.DB = settings["MySQL"]["db"]
        self.qt = settings["Settings"]["QueryTime"]

        self.db = db.Connection(
            host=self.HOST, port=self.PORT, user=self.USER,
            passwd=self.PASSWORD, db=self.DB)
        self.cur = self.db.cursor()

        self.query_string_headers = [
            "ID", "User", "Host", "DB", "State",
            "Query Time", "State", "Query"]

    def querycheck(self):
        self.cur.execute("show full processlist;")
        for row in self.cur.fetchall():
            try:
                if int(row[5]) > int(self.qt) and \
                        row[4] not in self.exclude_queries:
                    long_query = \
                        "ID: %s  User: %s Host: %s DB: %s State: %s \
                        Query Time: %s State: %s Query: %s" % (
                            row[0], row[1], row[2], row[3],
                            row[4], row[5], row[6], row[7])
                    self.all_queries.append(long_query)
            except TypeError:
                pass
        all_queries = filter(None, self.all_queries)
        if len(all_queries) >= 1:
            try:
                send_email_test(all_queries)
            except:
                import sys
                print("Issue with email, please check")
                sys.exit(1)
            try:
                record_to_file(all_queries)
            except IOError:
                import sys
                print("Error")
                print("Does log file exist? '{0}'".format(
                                settings["Logging"]["LogFile"]))
                sys.exit(1)
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    try:
        mysql = mysql_check()
        mysql.querycheck()
    except Exception as error:
        print(error)
