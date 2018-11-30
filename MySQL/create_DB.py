'''
 Copyright 2018 Leyang Yu yly@bu.edu

 This uses python 3.* and DO NOT support python 2.*
 This project requires tweepy, urllib, google.cloud, PILLOW and ffmpeg libraries.
 This project uses MySQL database to store picture information. 
 Setting up authentication for Google Cloud is REQUIRED before running this program.
'''
import mysql.connector
from mysql.connector import errorcode

# Please input your database user_name and password here.
DB_USER = 'user'
DB_PASSWORD = 'password'

# Choose Pics as working database.
DB_NAME = 'Pics'

TABLES = {}

# Define the contents in each table.
TABLES['pics_info'] = (
    "CREATE TABLE `pics_info` ("
    "  `Pic_No` int(10) NOT NULL,"
    "  `Screen_name` varchar(30) NOT NULL,"
    "  `pic_url` varchar(150) NOT NULL UNIQUE,"
    "  PRIMARY KEY (`Pic_No`)"
    ") ENGINE=InnoDB")

TABLES['tags'] = (
    "CREATE TABLE `tags` ("
    "  `tags_no` int(10) NOT NULL,"
    "  `tags` varchar(30) NOT NULL UNIQUE,"
    "  PRIMARY KEY (`tags_no`)"
    ") ENGINE=InnoDB")

TABLES['pic_tags'] = (
    "CREATE TABLE `pic_tags` ("
    "  `Pic_No` int(10) NOT NULL, "
    "  `tags_no` int(10) NOT NULL, "
    "  PRIMARY KEY (`Pic_No`,`tags_no`), KEY `Pic_No` (`Pic_No`),"
    "  KEY `tags_no` (`tags_no`),"
    "  FOREIGN KEY (`Pic_No`) REFERENCES `pics_info` (`Pic_No`) ON DELETE CASCADE, "
    "  FOREIGN KEY (`tags_no`) REFERENCES `tags` (`tags_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

# Connect to the database and create a cursor
cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD)
cursor = cnx.cursor()

# Check if user need to clean up an existing database or need to create a new database.
checker = input("Please input 0 if you need to clean up your existing database, and input 1 if you need to create a new database:")
if(checker == str(0)):
    cursor.execute("DROP DATABASE "+DB_NAME)

# Define the function to create a database
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# If the database dont exist, create it.
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

# Create tables in the database.
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
