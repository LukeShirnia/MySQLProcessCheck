# MySQLProcessCheck
Check MySQL process list with a python script.
<br />
This is python script to query MySQL processlist and report on all queries running over a certain defined time in seconds. These queries will then be emailed to a specified address.

<br />

### Overview
Python Script ---> Connects to MySQL
<br />
Checks "full processlist" query times
<br />
IF query time > x, send email
<br />


### Requirements
* Postfix configured to send mail locally
* Requires: mysql-python package

<br />

### Prerequisites
Before running the script you need to find and replace the following throughout the script:
* to@address.com ---> Address you wish to email long queries
* from@address.com ---> Address you are sending emails from
* int(row[5]) > 10 ---> Change 10 to the value in seconds you wish to use as the "long queries"
* exclude_queries = ['Sleep', 'Binlog Dump'] ---> Add all queries here you wish to exclude

<br />

### How to run
The Script is designed to run as a cron job:
<br />
Example: Run every 15 mins
```
*/15 * * * * /usr/bin/python /path/to/script/MySQLProcessCheck.py
```
<br />

### User Creation 
You can also create a MySQL user just for this script. I would suggest only granting the "select" and "process" priv to the user so they can view all mysql processes but have very limited access:
<br />
Example:
```
grant select, process on *.* to pcheck@localhost identified by 'long_random_password';
```
