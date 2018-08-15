# MySQLProcessCheck
Check MySQL process list with a python script.
<br />
This is python script to query MySQL processlist and report on all queries running over a certain defined time in seconds. These queries will then be emailed to a specified address and written to a file (with time stamps).

<br />

### Overview
Python Script ---> Connects to MySQL
<br />
Checks "full processlist" query times
<br />
IF query time > x, send email and log to file
<br />


### Requirements
* Postfix configured to send mail locally
* Requires: pyMYSQL

<br />

### Prerequisites
Before running the script you need to find and replace the following at the top of the script:

```
settings = {
    "Settings": {
        "QueryTime": 10  # In seconds
    },
    "MySQL": {
        "host": "127.0.0.1",  # MySQL bind address
        "port": 3306,         # MySQL port
        "user": "root",       # MySQL user
        "password": "",       # MySQL password
        "db": ""              # Leave blank to check all databases
    },
    "Email": {
        "Recipient": "",      # Where to send email
        "From": "",           # From email address
        "Subject": ""         # Subject
    },
    "Logging": {
        "LogFile": "/home/mysql/longqueries"  # Location to log queries
    },
    "Queries": [             # Exclude the following queries
        "Sleep",
        "Binlog Dump"
    ]
}
```


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
